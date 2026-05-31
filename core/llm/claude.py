"""
Claude adapter — uses Anthropic's SDK. Use this during local development.

This is the only file that imports the `anthropic` package. Nothing else in
the codebase knows or cares that Claude is being used.
"""
import os
from anthropic import Anthropic
from core.types import Message, LLMResponse, ToolCall


class ClaudeClient:
    def __init__(self, model: str = "claude-opus-4-7", api_key: str | None = None):
        self.model = model
        self.client = Anthropic(api_key=api_key or os.environ["ANTHROPIC_API_KEY"])

    def chat(
        self,
        messages: list[Message],
        system: str | None = None,
        tools: list[dict] | None = None,
        max_tokens: int = 4096,
    ) -> LLMResponse:
        kwargs = {
            "model": self.model,
            "max_tokens": max_tokens,
            "messages": self._to_anthropic_messages(messages),
        }
        if system:
            kwargs["system"] = system
        if tools:
            kwargs["tools"] = self._to_anthropic_tools(tools)

        resp = self.client.messages.create(**kwargs)
        return self._to_llm_response(resp)

    def chat_stream(
        self,
        messages: list[Message],
        system: str | None = None,
        tools: list[dict] | None = None,
        max_tokens: int = 4096,
    ):
        """
        Stream text chunks as they arrive, then yield the final LLMResponse.
        Yields: ("chunk", str) per text delta, then ("done", LLMResponse).
        """
        kwargs = {
            "model": self.model,
            "max_tokens": max_tokens,
            "messages": self._to_anthropic_messages(messages),
        }
        if system:
            kwargs["system"] = system
        if tools:
            kwargs["tools"] = self._to_anthropic_tools(tools)

        with self.client.messages.stream(**kwargs) as stream:
            for text in stream.text_stream:
                yield ("chunk", text)
            yield ("done", self._to_llm_response(stream.get_final_message()))

    # --- translation helpers -------------------------------------------------

    def _to_anthropic_messages(self, messages: list[Message]) -> list[dict]:
        result = []
        for msg in messages:
            if msg.role == "tool":
                # Tool results go in a user message with tool_result blocks
                result.append({
                    "role": "user",
                    "content": [
                        {
                            "type": "tool_result",
                            "tool_use_id": tr.tool_call_id,
                            "content": tr.content,
                        }
                        for tr in msg.tool_results
                    ],
                })
            elif msg.role == "assistant" and msg.tool_calls:
                content = []
                if msg.content:
                    content.append({"type": "text", "text": msg.content})
                for tc in msg.tool_calls:
                    content.append({
                        "type": "tool_use",
                        "id": tc.id,
                        "name": tc.name,
                        "input": tc.arguments,
                    })
                result.append({"role": "assistant", "content": content})
            else:
                result.append({"role": msg.role, "content": msg.content})
        return result

    def _to_anthropic_tools(self, tools: list[dict]) -> list[dict]:
        # OpenAI-style → Anthropic-style
        result = []
        for tool in tools:
            if tool.get("type") == "function":
                fn = tool["function"]
                result.append({
                    "name": fn["name"],
                    "description": fn.get("description", ""),
                    "input_schema": fn["parameters"],
                })
            else:
                result.append(tool)   # Pass through other tool types without modification but future consider validating or transforming them as needed
        return result

    def _to_llm_response(self, resp) -> LLMResponse:
        content_text = ""
        tool_calls = []
        for block in resp.content:
            if block.type == "text":
                content_text += block.text
            elif block.type == "tool_use":
                tool_calls.append(ToolCall(
                    id=block.id,
                    name=block.name,
                    arguments=block.input,
                ))
        return LLMResponse(
            content=content_text,
            tool_calls=tool_calls,
            stop_reason=resp.stop_reason or "end_turn",
            usage={
                "input_tokens": resp.usage.input_tokens,
                "output_tokens": resp.usage.output_tokens,
            },
        )
