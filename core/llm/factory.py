"""
LLM factory — picks an adapter based on config.yaml.

Switching providers is a one-line config change. No other code changes.
"""
import yaml
from pathlib import Path
from core.llm.base import LLMClient
from core.llm.claude import ClaudeClient
from core.llm.firm_internal import FirmInternalClient


def make_llm_client(config_path: str | Path = "config.yaml") -> LLMClient:
    cfg = yaml.safe_load(Path(config_path).read_text())["llm"]
    provider = cfg["provider"]

    if provider == "claude":
        return ClaudeClient(model=cfg.get("model", "claude-opus-4-7"))
    elif provider == "firm_internal":
        return FirmInternalClient(
            model=cfg.get("model", "firm-default"),
            base_url=cfg.get("base_url"),
        )
    else:  ## Need to add new providers here as we integrate them, but the rest of the codebase can remain unchanged.
        raise ValueError(
            f"Unknown LLM provider: {provider}. "
            f"Add it to core/llm/factory.py."
        )
