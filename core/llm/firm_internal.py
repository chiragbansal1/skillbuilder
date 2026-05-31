"""
Firm internal LLM adapter — STUB.

When you have access to your firm's LLM gateway, fill in chat() below.

Most firm gateways are OpenAI-compatible — in that case install `openai` and
point base_url at the gateway. Reference implementation in ClaudeClient
(core/llm/claude.py) shows how to handle tool translation if the gateway has
quirks.
"""
import os
from core.types import Message, LLMResponse, ToolCall


class FirmInternalClient:
    def __init__(
        self,
        model: str = "firm-default",
        base_url: str | None = None,
        api_key: str | None = None,
    ):
        self.model = model
        self.base_url = base_url or os.environ.get("FIRM_LLM_BASE_URL")
        self.api_key = api_key or os.environ.get("FIRM_LLM_API_KEY")

        # TODO: Initialize your firm's SDK or HTTP client here.
        #
        # If OpenAI-compatible:
        #   from openai import OpenAI
        #   self.client = OpenAI(base_url=self.base_url, api_key=self.api_key)
        #
        # If custom REST:
        #   import httpx
        #   self.client = httpx.Client(
        #       base_url=self.base_url,
        #       headers={"Authorization": f"Bearer {self.api_key}"},
        #   )

    def chat(
        self,
        messages: list[Message],
        system: str | None = None,
        tools: list[dict] | None = None,
        max_tokens: int = 4096,
    ) -> LLMResponse:
        # TODO: Implement using your firm's API.
        #
        # 1. Translate Message[] → firm's format. For OpenAI-style:
        #      [{"role": "system", "content": system}] + [
        #          {"role": m.role, "content": m.content} for m in messages
        #      ]
        #    (Tool calls/results need extra handling — see ClaudeClient
        #    for the full pattern.)
        #
        # 2. Call the API. For OpenAI-compatible:
        #      resp = self.client.chat.completions.create(
        #          model=self.model,
        #          messages=converted_messages,
        #          tools=tools,
        #          max_tokens=max_tokens,
        #      )
        #
        # 3. Parse response into LLMResponse:
        #      return LLMResponse(
        #          content=resp.choices[0].message.content or "",
        #          tool_calls=[
        #              ToolCall(id=tc.id, name=tc.function.name,
        #                       arguments=json.loads(tc.function.arguments))
        #              for tc in (resp.choices[0].message.tool_calls or [])
        #          ],
        #          stop_reason=_map_stop_reason(resp.choices[0].finish_reason),
        #          usage={
        #              "input_tokens": resp.usage.prompt_tokens,
        #              "output_tokens": resp.usage.completion_tokens,
        #          },
        #      )
        raise NotImplementedError(
            "FirmInternalClient.chat() is not yet implemented. "
            "Wire your firm's LLM API here — see ClaudeClient for a working reference."
        )

    def chat_stream(
        self,
        messages: list[Message],
        system: str | None = None,
        tools: list[dict] | None = None,
        max_tokens: int = 4096,
    ):
        # TODO: implement streaming for firm gateway.
        # For OpenAI-compatible gateways, use stream=True and iterate chunks.
        # Fall back to non-streaming for now:
        response = self.chat(messages=messages, system=system, tools=tools, max_tokens=max_tokens)
        yield ("chunk", response.content)
        yield ("done", response)
