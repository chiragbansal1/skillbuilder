"""
Run a skill from the database by ID.

Usage:
    python -m scripts.run_skill --id 1 --message "Summarise this NDA: ..."
    python -m scripts.run_skill              # falls back to built-in sample skill
"""
import argparse
import sys

from dotenv import load_dotenv
load_dotenv()

from core.llm.factory import make_llm_client
from core.mcp.factory import make_mcp_client
from core.executor.factory import make_executor
from core.storage.database import get_session
from core.storage.crud import get_skill_by_id, get_skill_files
from core.mcp.demo_tools import register_skill_tools


SAMPLE_SKILL = """
You are a helpful research assistant for an internal firm wiki.

When the user asks about a firm policy or process, use the `search_wiki` tool
to look it up, then summarise the result in 2-3 sentences in your own words.
If the wiki returns no useful info, say so plainly.
"""


def fake_wiki_search(query: str) -> str:
    fake_db = {
        "holiday": "Firm holiday policy: 25 days annual leave plus 10 national holidays. Carry-over up to 5 days. Approval required from line manager.",
        "expense": "Expenses up to $500 self-approve. Above $500 needs director sign-off. Submit via the expenses portal within 30 days.",
    }
    for key, value in fake_db.items():
        if key in query.lower():
            return value
    return "No matching wiki entry found."


def load_skill_from_db(skill_id: int) -> tuple[str, str]:
    """Return (skill_content, skill_name) for the given ID, appending attached files."""
    session = get_session()
    try:
        skill = get_skill_by_id(session, skill_id)
        if not skill:
            print(f"Error: no skill with id={skill_id} in the database.")
            sys.exit(1)

        content = skill.content

        files = get_skill_files(session, skill_id)
        if files:
            content += "\n\n---\n## Attached reference files\n"
            for f in files:
                content += f"\n### {f.filename}\n{f.content}\n"

        return content, skill.name
    finally:
        session.close()


def build_stack():
    llm = make_llm_client()
    mcp = make_mcp_client()
    executor = make_executor(llm=llm, mcp=mcp)
    return llm, mcp, executor


def main():
    parser = argparse.ArgumentParser(description="Run a skill end-to-end.")
    parser.add_argument("--id", type=int, dest="skill_id", help="Skill ID to load from the database")
    parser.add_argument("--message", type=str, default=None, help="User message to send to the skill")
    args = parser.parse_args()

    llm, mcp, executor = build_stack()

    if args.skill_id is not None:
        skill_content, skill_name = load_skill_from_db(args.skill_id)
        user_message = args.message or "Hello! What can you help me with?"
        print(f"Skill:    {skill_name} (id={args.skill_id})")
    else:
        skill_content = SAMPLE_SKILL
        skill_name = "sample"
        user_message = args.message or "What's our holiday policy?"
        print(f"Skill:    {skill_name} (built-in sample)")

    registered = register_skill_tools(mcp, skill_content)

    print(f"LLM:      {llm.__class__.__name__}")
    print(f"MCP:      {mcp.__class__.__name__}")
    print(f"Executor: {executor.__class__.__name__}")
    if registered:
        print(f"Tools:    {', '.join(registered)}")
    print("---")
    print(f"User: {user_message}\n")

    for event in executor.run(skill_content=skill_content, user_message=user_message):
        if event.type == "text":
            print(f"Assistant: {event.data['text']}")
        elif event.type == "tool_call":
            print(f"[tool_call] {event.data['name']}({event.data['arguments']})")
        elif event.type == "tool_result":
            print(f"[tool_result] {event.data['content']}")
        elif event.type == "done":
            print(f"[done] reason={event.data.get('reason')}")
        elif event.type == "error":
            print(f"[error] {event.data.get('message')}", file=sys.stderr)


if __name__ == "__main__":
    main()
