"""
LocalToolsClient — register Python functions as tools without spinning up an MCP server.

Use this for hackathon development and demos. Implements the same MCPClient
protocol as a real MCP client, so swapping later is one factory line.
"""
from typing import Callable


class LocalToolsClient:
    def __init__(self):
        self._tools: dict[str, dict] = {}

    def register(
        self,
        name: str,
        description: str,
        parameters: dict,
        fn: Callable[..., str],
    ):
        """Register a Python function as a callable tool."""
        self._tools[name] = {
            "description": description,
            "parameters": parameters,
            "fn": fn,
        }

    def connect_servers(self, servers: list[dict]) -> None:
        # No-op — tools are pre-registered in Python, no servers to connect to.
        pass

    def list_tools_as_openai_schema(self) -> list[dict]:
        return [
            {
                "type": "function",
                "function": {
                    "name": name,
                    "description": t["description"],
                    "parameters": t["parameters"],
                },
            }
            for name, t in self._tools.items()
        ]

    def execute_tool(self, tool_name: str, arguments: dict) -> str:
        if tool_name not in self._tools:
            return f"Error: tool '{tool_name}' not found"
        try:
            return str(self._tools[tool_name]["fn"](**arguments))
        except Exception as e:
            return f"Error executing {tool_name}: {e}"
