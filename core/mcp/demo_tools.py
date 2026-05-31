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


def _get_employee_info(employee_name: str) -> str:
    db = {
        "tyrion": (
            "Name: Tyrion Lannister | Role: Senior Legal Counsel | Team: Legal & Compliance | "
            "Manager: Tywin Lannister | Start Date: June 10, 2026 | Office: London | "
            "Grade: L5 | Employment Type: Full-time | "
            "Key Responsibilities: Contract negotiation, NDA review, regulatory compliance, IP advisory. "
            "Tools Access: LegalVault, ContractPro, Westlaw. "
            "Pending Setup: Bar membership verification, security clearance (Level 2), DocuSign access. "
            "First Week: Meet Cersei (Head of Legal) on Day 1, complete compliance training by Day 3, "
            "shadow NDA review process by Day 5. "
            "Perks: London transport allowance £150/month, home office stipend £500 one-time, "
            "legal journal subscriptions covered."
        ),
        "jamie": (
            "Name: Jamie Lannister | Role: Enterprise Sales Executive | Team: Enterprise Sales | "
            "Manager: Tywin Lannister | Start Date: June 15, 2026 | Office: New York | "
            "Grade: S4 | Employment Type: Full-time | "
            "Key Responsibilities: Enterprise account management, new business development, "
            "RFP responses, CRM pipeline management. "
            "Tools Access: Salesforce, Gong, LinkedIn Sales Navigator, Tableau. "
            "Pending Setup: Salesforce license assignment, Gong call recording consent, "
            "corporate Amex card. "
            "First Week: Sales bootcamp Day 1-2, shadow senior AE on 3 calls, "
            "complete product certification by Day 5. "
            "Perks: Sales commission plan (10% on new business), NYC commuter benefit $300/month, "
            "phone allowance $80/month."
        ),
        "cersei": (
            "Name: Cersei Lannister | Role: Head of Legal | Team: Legal & Compliance | "
            "Manager: Robert Baratheon (CEO) | Start Date: March 1, 2019 | Office: London | "
            "Grade: L8 | Employment Type: Full-time | "
            "Key Responsibilities: Legal strategy, M&A oversight, board governance, "
            "regulatory relationships, team leadership (12 reports). "
            "Tools Access: All legal systems, board portal, M&A dataroom. "
            "Direct Reports: Tyrion Lannister, Sansa Stark, Brienne of Tarth. "
            "Perks: Executive package — private health, car allowance £800/month, "
            "annual equity grant, executive coaching budget £5,000/year."
        ),
        "daenerys": (
            "Name: Daenerys Targaryen | Role: VP of Product | Team: Product Management | "
            "Manager: Robert Baratheon (CEO) | Start Date: January 15, 2024 | Office: Remote (Essos) | "
            "Grade: P8 | Employment Type: Full-time | "
            "Key Responsibilities: Product vision and roadmap, cross-functional leadership, "
            "OKR setting, market strategy, partnerships. "
            "Tools Access: Jira, Figma, Amplitude, Notion, all product dashboards. "
            "Direct Reports: Jon Snow, Missandei, Grey Worm. "
            "Perks: Full remote approved, home office budget $2,000/year, "
            "international travel budget $15,000/year, equity (0.8% vested over 4 years)."
        ),
        "jon": (
            "Name: Jon Snow | Role: Senior Product Manager | Team: Product Management | "
            "Manager: Daenerys Targaryen | Start Date: September 1, 2025 | Office: Edinburgh | "
            "Grade: P5 | Employment Type: Full-time | "
            "Key Responsibilities: Skill execution product area, roadmap ownership, "
            "user research, sprint planning, stakeholder alignment. "
            "Tools Access: Jira, Confluence, Figma, Mixpanel, Notion. "
            "Pending Setup: Figma seat, Amplitude access, product analytics dashboard. "
            "First Week: Onboarding with Daenerys Day 1, product deep-dive sessions Day 2-3, "
            "meet engineering lead (Sam) Day 4, first sprint planning Day 5. "
            "Perks: Edinburgh flexible office access, learning budget £2,000/year."
        ),
        "arya": (
            "Name: Arya Stark | Role: Senior Security Engineer | Team: Platform Engineering | "
            "Manager: Harish Guragol | Start Date: April 5, 2026 | Office: Bangalore | "
            "Grade: E6 | Employment Type: Full-time | "
            "Key Responsibilities: Penetration testing, threat modelling, security reviews, "
            "incident response, zero-trust architecture. "
            "Tools Access: AWS Security Hub, Burp Suite, Splunk, PagerDuty, GitHub (admin). "
            "Pending Setup: VPN certificate, HSM access, AWS IAM role assignment. "
            "First Week: Security systems orientation Day 1, threat model review Day 2, "
            "shadow on-call rotation Day 3-5. "
            "Perks: Bug bounty participation allowed, security conference budget $3,000/year, "
            "home lab equipment reimbursement up to $1,500."
        ),
        "sansa": (
            "Name: Sansa Stark | Role: Legal Operations Manager | Team: Legal & Compliance | "
            "Manager: Cersei Lannister | Start Date: July 20, 2023 | Office: London | "
            "Grade: L4 | Employment Type: Full-time | "
            "Key Responsibilities: Contract lifecycle management, legal ops tooling, "
            "vendor management, process improvement, paralegal team oversight. "
            "Tools Access: ContractPro, DocuSign, LegalVault, Asana. "
            "Direct Reports: 3 paralegals. "
            "Perks: London office perks, flexible working 2 days remote, "
            "professional development budget £1,500/year."
        ),
        "sam": (
            "Name: Samwell Tarly | Role: Engineering Manager | Team: Platform Engineering | "
            "Manager: Harish Guragol | Start Date: February 10, 2022 | Office: Bangalore | "
            "Grade: E7 | Employment Type: Full-time | "
            "Key Responsibilities: Team leadership (8 engineers), technical roadmap, "
            "architecture decisions, hiring, cross-team coordination. "
            "Tools Access: All engineering systems, AWS console (admin), GitHub (org admin). "
            "Direct Reports: Arya Stark, Grey Worm, Podrick Payne, 5 others. "
            "Perks: Engineering conference budget $4,000/year, AWS certification reimbursement, "
            "equity grant (refresher), management coaching sessions."
        ),
        "missandei": (
            "Name: Missandei | Role: Head of People & Culture | Team: HR | "
            "Manager: Robert Baratheon (CEO) | Start Date: May 1, 2021 | Office: London | "
            "Grade: HR8 | Employment Type: Full-time | "
            "Key Responsibilities: Talent acquisition strategy, L&D, DEI programmes, "
            "compensation benchmarking, employee relations, culture initiatives. "
            "Tools Access: Workday, Greenhouse, Culture Amp, LinkedIn Talent. "
            "Direct Reports: 5 HR business partners. "
            "Perks: Full executive package, DEI conference budget £3,000/year."
        ),
        "brienne": (
            "Name: Brienne of Tarth | Role: Compliance Officer | Team: Legal & Compliance | "
            "Manager: Cersei Lannister | Start Date: November 12, 2022 | Office: London | "
            "Grade: L5 | Employment Type: Full-time | "
            "Key Responsibilities: Regulatory compliance (FCA, GDPR), audit management, "
            "policy enforcement, compliance training, incident reporting. "
            "Tools Access: ComplyAdvantage, OneTrust, LegalVault, Workday. "
            "Perks: ICA certification sponsorship, compliance conference budget £2,000/year."
        ),
    }
    name = employee_name.lower()
    for key, value in db.items():
        if key in name:
            return value
    return (
        f"No employee record found for '{employee_name}'. "
        "Please check the spelling or contact HR (Missandei) directly."
    )


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
    "get_employee_info": {
        "name": "get_employee_info",
        "description": "Look up employee details including role, team, manager, office, tools access, and onboarding info.",
        "parameters": {
            "type": "object",
            "properties": {
                "employee_name": {
                    "type": "string",
                    "description": "First name or full name of the employee",
                },
            },
            "required": ["employee_name"],
        },
        "fn": _get_employee_info,
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
