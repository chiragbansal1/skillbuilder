"""
GenericExecutor — LLM-agnostic skill executor.

Works with any LLMClient (Claude, firm gateway, OpenAI, anything) because it
only uses the protocol interface. Implements the tool-use loop manually so it
doesn't depend on any provider's native MCP support.
"""
from typing import Iterator
from core.types import Message, ToolResult
from core.executor.base import Event
from core.llm.base import LLMClient
from core.mcp.base import MCPClient


class GenericExecutor:
    def __init__(self, llm: LLMClient, mcp: MCPClient, max_turns: int = 10):
        self.llm = llm
        self.mcp = mcp
        self.max_turns = max_turns

    def run(
        self,
        skill_content: str,
        user_message: str,
        mcp_servers: list[dict] | None = None,
        history: list[dict] | None = None,
    ) -> Iterator[Event]:
        # Connect MCP servers if any (no-op for LocalToolsClient)
        if mcp_servers:
            self.mcp.connect_servers(mcp_servers)
        tools = self.mcp.list_tools_as_openai_schema()

        # Build message list: prior conversation history + current user message
        messages: list[Message] = [
            Message(role=m["role"], content=m["content"])
            for m in (history or [])
        ]
        messages.append(Message(role="user", content=user_message))

        for _ in range(self.max_turns):
            response = self.llm.chat(
                messages=messages,
                system=skill_content,
                tools=tools if tools else None,
            )

            if response.content:
                yield Event(type="text", data={"text": response.content})

            if not response.tool_calls:
                yield Event(type="done", data={"reason": "end_turn"})
                return

            # Record assistant turn (text + tool calls) so the LLM sees context next turn
            messages.append(Message(
                role="assistant",
                content=response.content,
                tool_calls=response.tool_calls,
            ))

            # Execute each requested tool
            results = []
            for call in response.tool_calls:
                yield Event(type="tool_call", data={
                    "id": call.id,
                    "name": call.name,
                    "arguments": call.arguments,
                })
                result_str = self.mcp.execute_tool(call.name, call.arguments)
                results.append(ToolResult(tool_call_id=call.id, content=result_str))
                yield Event(type="tool_result", data={
                    "id": call.id,
                    "content": result_str,
                })

            messages.append(Message(role="tool", tool_results=results))

        yield Event(type="done", data={"reason": "max_turns_reached"})
