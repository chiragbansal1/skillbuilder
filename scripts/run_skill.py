"""
End-to-end test — runs a sample skill that uses a tool.

This exercises every layer: factory → LLM adapter → executor → MCP client → tool.
If this works, swapping the LLM provider later requires only a config.yaml change.

Run: python -m scripts.run_skill
"""
from dotenv import load_dotenv
load_dotenv()

from core.llm.factory import make_llm_client
from core.mcp.local_tools import LocalToolsClient
from core.executor.factory import make_executor


SAMPLE_SKILL = """
You are a helpful research assistant for an internal firm wiki.

When the user asks about a firm policy or process, use the `search_wiki` tool
to look it up, then summarise the result in 2-3 sentences in your own words.
If the wiki returns no useful info, say so plainly.
"""


def fake_wiki_search(query: str) -> str:
    """Pretend wiki — replace with a real lookup or an MCP server later."""
    fake_db = {
        "holiday": "Firm holiday policy: 25 days annual leave plus 10 national holidays. Carry-over up to 5 days. Approval required from line manager.",
        "expense": "Expenses up to $500 self-approve. Above $500 needs director sign-off. Submit via the expenses portal within 30 days.",
    }
    for key, value in fake_db.items():
        if key in query.lower():
            return value
    return "No matching wiki entry found."


def main():
    # Build the stack from config
    llm = make_llm_client()
    mcp = LocalToolsClient()
    mcp.register(
        name="search_wiki",
        description="Search the internal firm wiki for a policy or process.",
        parameters={
            "type": "object",
            "properties": {"query": {"type": "string", "description": "Search query"}},
            "required": ["query"],
        },
        fn=fake_wiki_search,
    )
    executor = make_executor(llm=llm, mcp=mcp)

    print(f"LLM:      {llm.__class__.__name__}")
    print(f"MCP:      {mcp.__class__.__name__}")
    print(f"Executor: {executor.__class__.__name__}")
    print("---")

    user_message = "What's our holiday policy?"
    print(f"User: {user_message}\n")

    for event in executor.run(skill_content=SAMPLE_SKILL, user_message=user_message):
        if event.type == "text":
            print(f"Assistant: {event.data['text']}")
        elif event.type == "tool_call":
            print(f"[tool_call] {event.data['name']}({event.data['arguments']})")
        elif event.type == "tool_result":
            print(f"[tool_result] {event.data['content']}")
        elif event.type == "done":
            print(f"[done] reason={event.data.get('reason')}")


if __name__ == "__main__":
    main()
