"""
LLMClient protocol — the contract every LLM adapter must implement.

To add a new provider:
1. Create a new file in core/llm/ (e.g., bedrock.py)
2. Implement a class with a chat() method matching this signature
3. Register it in core/llm/factory.py

The chat() method always:
  - Accepts our generic Message[] format
  - Accepts an OpenAI-style tool schema (most portable format)
  - Returns our generic LLMResponse
The adapter handles all translation to/from the provider's native format.
"""
from typing import Protocol, runtime_checkable
from core.types import Message, LLMResponse


@runtime_checkable
class LLMClient(Protocol):
    def chat(
        self,
        messages: list[Message],
        system: str | None = None,
        tools: list[dict] | None = None,
        max_tokens: int = 4096,
    ) -> LLMResponse: ...
