"""
MCP factory — picks a client implementation based on config.yaml.

Switching MCP implementations is a one-line config change. No other code changes.
"""
import yaml
from pathlib import Path
from core.mcp.base import MCPClient
from core.mcp.local_tools import LocalToolsClient


def make_mcp_client(config_path: str | Path = "config.yaml") -> MCPClient:
    cfg = yaml.safe_load(Path(config_path).read_text()).get("mcp", {})
    mcp_type = cfg.get("type", "local")

    if mcp_type == "local":
        return LocalToolsClient()
    else:
        raise ValueError(
            f"Unknown MCP type: {mcp_type}. "
            f"Add it to core/mcp/factory.py."
        )
