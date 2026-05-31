"""
Demo tool implementations for the hackathon.

Each entry in TOOL_REGISTRY is a dict ready to be unpacked into
LocalToolsClient.register(). Skills declare which tools they need via
  tools: [search_wiki, lookup_contract]
in their SKILL.md frontmatter, and register_skill_tools() wires them up.

When the firm provides real MCP servers, this file is replaced by
RemoteMCPClient.connect_servers() — nothing else in the stack changes.
"""
import re
import yaml
from core.mcp.base import MCPClient


# ── Fake tool implementations ────────────────────────────────────────────────

def _search_wiki(query: str) -> str:
    db = {
        "holiday": (
            "Holiday policy: 25 days annual leave plus 10 national holidays. "
            "Up to 5 days carry-over with manager approval."
        ),
        "expense": (
            "Expenses up to $500 are self-approved. Above $500 requires director sign-off. "
            "Submit via the expenses portal within 30 days of incurring the cost."
        ),
        "remote": (
            "Remote working: up to 3 days per week. Core hours are 10am–3pm local time. "
            "Full remote requires VP approval."
        ),
        "bonus": (
            "Annual bonus paid in March, based on individual rating and firm performance. "
            "Target is 10–20% of base salary."
        ),
        "parental": (
            "Parental leave: 26 weeks full pay for primary caregiver, "
            "4 weeks full pay for secondary caregiver."
        ),
        "travel": (
            "Business travel: economy for flights under 6 hours, business class above. "
            "Hotel budget $250/night in major cities, $150 elsewhere."
        ),
    }
    for key, value in db.items():
        if key in query.lower():
            return value
    return "No matching wiki entry found for that query."


def _lookup_contract(counterparty: str) -> str:
    db = {
        "acme": (
            "Acme Corp — 2 prior NDAs (signed 2021, 2023, both expired). "
            "Active MSA since 2022. No disputes on record. Preferred vendor status."
        ),
        "globex": (
            "Globex Inc — 1 prior NDA (2022, expired). MSA expired 2024. "
            "Dispute logged 2023 over IP ownership — resolved via mediation."
        ),
        "initech": (
            "Initech Ltd — no prior contracts. First engagement. "
            "Referred by internal legal team."
        ),
        "umbrella": (
            "Umbrella Solutions — 3 prior NDAs. Active partnership agreement. "
            "Note: NDA from 2020 had non-standard jurisdiction clause (Delaware)."
        ),
    }
    name = counterparty.lower()
    for key, value in db.items():
        if key in name:
            return value
    return f"No prior contract history found for '{counterparty}'."


# ── Registry ──────────────────────────────────────────────────────────────────

TOOL_REGISTRY: dict[str, dict] = {
    "search_wiki": {
        "name": "search_wiki",
        "description": "Search the internal firm wiki for policies, processes, and procedures.",
        "parameters": {
            "type": "object",
            "properties": {
                "query": {"type": "string", "description": "Search term or topic"},
            },
            "required": ["query"],
        },
        "fn": _search_wiki,
    },
    "lookup_contract": {
        "name": "lookup_contract",
        "description": "Look up prior contract history for a named counterparty.",
        "parameters": {
            "type": "object",
            "properties": {
                "counterparty": {
                    "type": "string",
                    "description": "Name of the company or individual to look up",
                },
            },
            "required": ["counterparty"],
        },
        "fn": _lookup_contract,
    },
}


# ── Helper ────────────────────────────────────────────────────────────────────

def register_skill_tools(mcp: MCPClient, skill_content: str) -> list[str]:
    """
    Parse the skill's frontmatter for a `tools` list, register each known
    tool with the MCP client, and return the names that were registered.
    """
    match = re.match(r"^---\n(.*?)\n---", skill_content, re.DOTALL)
    if not match:
        return []
    try:
        meta = yaml.safe_load(match.group(1)) or {}
    except yaml.YAMLError:
        return []

    requested = meta.get("tools", [])
    registered = []
    for name in requested:
        if name in TOOL_REGISTRY:
            mcp.register(**TOOL_REGISTRY[name])
            registered.append(name)
    return registered
