"""
Gemini adapter — uses direct REST API requests.
No extra SDK packages required. Works with any standard httpx or requests installation.
"""
import os
import uuid
import httpx
from core.types import Message, LLMResponse, ToolCall


class GeminiClient:
    def __init__(self, model: str = "gemini-2.5-flash", api_key: str | None = None):
        self.model = model
        self.api_key = api_key or os.environ.get("GEMINI_API_KEY")
        if not self.api_key:
            raise ValueError("GEMINI_API_KEY environment variable is not set")
        self.base_url = "https://generativelanguage.googleapis.com/v1beta"

    def chat(
        self,
        messages: list[Message],
        system: str | None = None,
        tools: list[dict] | None = None,
        max_tokens: int = 4096,
    ) -> LLMResponse:
        url = f"{self.base_url}/models/{self.model}:generateContent?key={self.api_key}"
        
        payload = {
            "contents": self._to_gemini_contents(messages),
        }
        
        if system:
            payload["systemInstruction"] = {
                "parts": [{"text": system}]
            }
            
        if tools:
            gemini_tools = self._to_gemini_tools(tools)
            if gemini_tools:
                payload["tools"] = gemini_tools

        # Configure generation config
        payload["generationConfig"] = {
            "maxOutputTokens": max_tokens,
            "temperature": 0.2,
        }

        resp = httpx.post(url, json=payload, timeout=60.0)
        if resp.status_code != 200:
            raise ValueError(f"Gemini API returned error {resp.status_code}: {resp.text}")
            
        return self._to_llm_response(resp.json())

    def chat_stream(
        self,
        messages: list[Message],
        system: str | None = None,
        tools: list[dict] | None = None,
        max_tokens: int = 4096,
    ):
        """
        Stream text chunks as they arrive by simulating chunking from the complete response.
        Ensures perfect reliability without stream framing complexity.
        """
        response = self.chat(messages, system, tools, max_tokens)
        content = response.content
        if content:
            # Yield in small pieces to show progressive typing in UI
            chunk_size = 24
            for i in range(0, len(content), chunk_size):
                yield ("chunk", content[i : i + chunk_size])
        yield ("done", response)

    # --- translation helpers -------------------------------------------------

    def _normalize_schema_types(self, schema: dict) -> dict:
        """Recursively convert schema types to uppercase as required by Gemini API."""
        if not isinstance(schema, dict):
            return schema
        new_schema = {}
        for k, v in schema.items():
            if k == "type" and isinstance(v, str):
                new_schema[k] = v.upper()
            elif isinstance(v, dict):
                new_schema[k] = self._normalize_schema_types(v)
            elif isinstance(v, list):
                new_schema[k] = [
                    self._normalize_schema_types(item) if isinstance(item, dict) else item
                    for item in v
                ]
            else:
                new_schema[k] = v
        return new_schema

    def _to_gemini_contents(self, messages: list[Message]) -> list[dict]:
        result = []
        # Build a mapping of tool call IDs to names from past assistant turns
        tool_id_to_name = {}
        for msg in messages:
            for tc in msg.tool_calls:
                tool_id_to_name[tc.id] = tc.name

        for msg in messages:
            if msg.role == "user":
                result.append({
                    "role": "user",
                    "parts": [{"text": msg.content}]
                })
            elif msg.role in ("assistant", "model"):
                parts = []
                if msg.content:
                    parts.append({"text": msg.content})
                for tc in msg.tool_calls:
                    parts.append({
                        "functionCall": {
                            "name": tc.name,
                            "args": tc.arguments
                        }
                    })
                result.append({
                    "role": "model",
                    "parts": parts
                })
            elif msg.role == "tool":
                parts = []
                for tr in msg.tool_results:
                    tool_name = tool_id_to_name.get(tr.tool_call_id, "unknown_tool")
                    parts.append({
                        "functionResponse": {
                            "name": tool_name,
                            "response": {
                                "output": tr.content
                            }
                        }
                    })
                result.append({
                    "role": "function",
                    "parts": parts
                })
        return result

    def _to_gemini_tools(self, tools: list[dict]) -> list[dict]:
        declarations = []
        for tool in tools:
            if tool.get("type") == "function":
                fn = tool["function"]
                declarations.append({
                    "name": fn["name"],
                    "description": fn.get("description", ""),
                    "parameters": self._normalize_schema_types(fn.get("parameters", {}))
                })
        if declarations:
            return [{"functionDeclarations": declarations}]
        return []

    def _to_llm_response(self, resp_json: dict) -> LLMResponse:
        content_text = ""
        tool_calls = []
        candidates = resp_json.get("candidates", [])
        
        if candidates:
            candidate = candidates[0]
            content = candidate.get("content", {})
            parts = content.get("parts", [])
            for part in parts:
                if "text" in part:
                    content_text += part["text"]
                elif "functionCall" in part:
                    fc = part["functionCall"]
                    # Generate a unique tool call ID since REST does not enforce one
                    call_id = f"call_{uuid.uuid4().hex[:8]}"
                    tool_calls.append(ToolCall(
                        id=call_id,
                        name=fc["name"],
                        arguments=fc.get("args", {}),
                    ))
            
            finish_reason = candidate.get("finishReason", "STOP")
            stop_reason = "end_turn"
            if finish_reason == "STOP":
                if tool_calls:
                    stop_reason = "tool_use"
                else:
                    stop_reason = "end_turn"
            elif finish_reason == "MAX_TOKENS":
                stop_reason = "max_tokens"
            else:
                stop_reason = "other"
        else:
            stop_reason = "other"

        return LLMResponse(
            content=content_text,
            tool_calls=tool_calls,
            stop_reason=stop_reason,
            usage=resp_json.get("usageMetadata", {}),
        )
