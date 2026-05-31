"""
AgentExecutor protocol — runs a skill to completion, yielding events as they happen.

Different executors can use different strategies (manual tool loop, native MCP
connector, etc.) but they all expose the same interface so the UI stays simple.
"""
from typing import Protocol, Iterator, runtime_checkable
from pydantic import BaseModel


class Event(BaseModel):
    type: str  # "text" | "tool_call" | "tool_result" | "done" | "error"
    data: dict = {}


@runtime_checkable
class AgentExecutor(Protocol):
    def run(
        self,
        skill_content: str,
        user_message: str,
        mcp_servers: list[dict] | None = None,
        history: list[dict] | None = None,
    ) -> Iterator[Event]: ...
