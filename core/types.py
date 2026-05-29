"""
Provider-agnostic types used everywhere in the codebase.

Every LLM adapter accepts these types and translates them to its native format
internally. This is what makes the system swappable.
"""
from typing import Literal
from pydantic import BaseModel, Field


class ToolCall(BaseModel):
    id: str
    name: str
    arguments: dict


class ToolResult(BaseModel):
    tool_call_id: str
    content: str


class Message(BaseModel):
    role: Literal["user", "assistant", "tool"]
    content: str = ""
    tool_calls: list[ToolCall] = Field(default_factory=list)
    tool_results: list[ToolResult] = Field(default_factory=list)


class LLMResponse(BaseModel):
    content: str
    tool_calls: list[ToolCall] = Field(default_factory=list)
    stop_reason: Literal[
        "end_turn", "tool_use", "max_tokens", "stop_sequence", "other"
    ] = "end_turn"
    usage: dict = Field(default_factory=dict)
