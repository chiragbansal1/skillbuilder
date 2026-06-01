"""
LLM factory — picks an adapter based on config.yaml.

Switching providers is a one-line config change. No other code changes.
"""
import yaml
from pathlib import Path
from core.llm.base import LLMClient
from core.llm.claude import ClaudeClient
from core.llm.gemini import GeminiClient
from core.llm.firm_internal import FirmInternalClient


def make_llm_client(config_path: str | Path = "config.yaml") -> LLMClient:
    import os
    import streamlit as st
    
    # Default settings
    try:
        cfg = yaml.safe_load(Path(config_path).read_text())["llm"]
    except Exception:
        cfg = {"provider": "gemini", "model": "gemini-2.5-flash"}
        
    provider = cfg.get("provider", "gemini")
    model = cfg.get("model", "gemini-2.5-flash")
    
    # Overrides from streamlit session state
    try:
        if "llm_provider" in st.session_state:
            provider = st.session_state["llm_provider"]
            if provider == "gemini":
                model = "gemini-2.5-flash"
            elif provider == "claude":
                model = "claude-opus-4-7"
            else:
                model = "mock-default"
    except Exception:
        pass
        
    # Keys checking
    gemini_key = os.environ.get("GEMINI_API_KEY")
    anthropic_key = os.environ.get("ANTHROPIC_API_KEY")
    
    try:
        if "gemini_api_key" in st.session_state and st.session_state["gemini_api_key"]:
            gemini_key = st.session_state["gemini_api_key"]
        if "anthropic_api_key" in st.session_state and st.session_state["anthropic_api_key"]:
            anthropic_key = st.session_state["anthropic_api_key"]
    except Exception:
        pass

    # If Claude is selected but no API key exists, automatically fall back to Mock LLM
    if provider == "claude" and not anthropic_key:
        from core.llm.mock import MockLLMClient
        return MockLLMClient(model="mock-claude-fallback")

    # If Gemini is selected but no API key exists, automatically fall back to Mock LLM
    if provider == "gemini" and not gemini_key:
        from core.llm.mock import MockLLMClient
        return MockLLMClient(model="mock-gemini-fallback")

    if provider == "mock":
        from core.llm.mock import MockLLMClient
        return MockLLMClient(model=model)
    elif provider == "claude":
        return ClaudeClient(model=model, api_key=anthropic_key)
    elif provider == "gemini":
        return GeminiClient(model=model, api_key=gemini_key)
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
