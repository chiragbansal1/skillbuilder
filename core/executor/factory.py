"""Executor factory — selects the executor implementation from config."""
import yaml
from pathlib import Path
from core.executor.base import AgentExecutor
from core.executor.generic import GenericExecutor
from core.llm.base import LLMClient
from core.mcp.base import MCPClient


def make_executor(
    llm: LLMClient,
    mcp: MCPClient,
    config_path: str | Path = "config.yaml",
) -> AgentExecutor:
    cfg = yaml.safe_load(Path(config_path).read_text()).get("executor", {})
    executor_type = cfg.get("type", "generic")
    max_turns = cfg.get("max_turns", 10)

    if executor_type == "generic":
        return GenericExecutor(llm=llm, mcp=mcp, max_turns=max_turns)
    else:
        raise ValueError(f"Unknown executor type: {executor_type}")
