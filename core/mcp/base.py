"""
MCPClient protocol — abstracts the source of tools.

Today: LocalToolsClient (in-memory Python functions, no MCP server needed).
Tomorrow: RemoteMCPClient using the official `mcp` Python SDK.

The executor only talks to this protocol — it doesn't know or care which is in use.
"""
from typing import Protocol, runtime_checkable


@runtime_checkable
class MCPClient(Protocol):
    def connect_servers(self, servers: list[dict]) -> None:
        """Connect to the given MCP servers. No-op if not using remote MCP."""
        ...

    def list_tools_as_openai_schema(self) -> list[dict]:
        """Return all available tools in OpenAI function-calling JSON schema format."""
        ...

    def execute_tool(self, tool_name: str, arguments: dict) -> str:
        """Execute a tool by name with arguments and return its string result."""
        ...
