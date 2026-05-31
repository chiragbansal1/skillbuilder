# CLAUDE.md — Project Context for Claude Code

## What is this project?

SkillForge is a hackathon project for our firm. It's a web app where anyone in
the firm — technical or not — can create, share, update, and execute Claude-style
"skills" through a guided conversational interface. Think "GitHub for skills,
but with a no-code builder."

A "skill" is a structured set of instructions (a SKILL.md file) that tells an
LLM how to perform a specific task — like summarising contracts, formatting
meeting notes, or searching the firm wiki. Skills are created via a chat-based
interview, stored in a database, browsable in a library, and executable by
anyone.

## Key constraints

- **LLM-agnostic**: The firm can't use Claude API directly in production. Today
  we develop locally with Claude API, but the architecture MUST allow swapping
  to any LLM provider (firm's internal gateway, OpenAI, Bedrock, etc.) with
  only a config change. No provider SDK should be imported outside its adapter
  file.
- **MCP-agnostic**: Skills can use MCP tools, but the MCP layer is also
  abstracted. Today we use `LocalToolsClient` (in-memory Python functions).
  Later this swaps to a real MCP client using the `mcp` Python SDK.
- **Mixed audience**: Users range from non-technical (legal, sales) to
  developers. UI and language should be accessible to both.

## Architecture

Three pluggable layers, each behind a Python Protocol:

```
LLMClient (core/llm/base.py)
  └── Wraps a chat-completion API
  └── Implementations: claude.py (live), firm_internal.py (stub)

MCPClient (core/mcp/base.py)
  └── Provides tools to the executor
  └── Implementations: local_tools.py (in-memory, no MCP server needed)

AgentExecutor (core/executor/base.py)
  └── Runs a skill: loads SKILL.md into system prompt, manages tool-use loop
  └── Implementations: generic.py (works with any LLMClient)
```

Storage layer (core/storage/):

```
models.py    — Skill, SkillVersion, SkillFile SQLModel table definitions
database.py  — SQLite engine, create_db_and_tables(), get_session()
crud.py      — create_skill, get_skill_by_id, list_skills, update_skill,
               delete_skill, add_skill_file, get_skill_files,
               delete_skill_files, list_skill_versions
```

File extraction layer (core/files.py):
```
extract_text(filename, bytes) — converts PDF, Excel, CSV, code to plain text
file_type_label(filename)     — returns "code" or "doc" based on extension
```

Demo tools (core/mcp/demo_tools.py):
```
TOOL_REGISTRY          — fake tool implementations: search_wiki, lookup_contract
register_skill_tools() — parses skill frontmatter and registers declared tools
```

Shared constants (shared.py):
```
FAKE_USERS — list of demo personas used across all pages
```

Each skill folder under skills/ contains:
- `SKILL.md`   — the instructions (becomes the system prompt at runtime)
- `skill.json` — manifest: name, description, author, attached files list
- `reference/` — optional documentation, code, or tool files attached to the skill

Config-driven via `config.yaml`. Factories in each layer read the config and
return the right implementation.

**Design rule**: `anthropic` SDK is imported ONLY in `core/llm/claude.py`.
Nothing else in the codebase should reference any provider directly. If you
need to add a new provider, create a new adapter file and register it in the
factory. DO NOT scatter provider-specific code into the executor, UI, or storage
layers.

Tools use OpenAI-style JSON schemas internally (most portable format). Each LLM
adapter translates to its native format as needed.

## Development plan (phases)

### Phase 0-1: Foundation + LLM abstraction ✅ DONE
Project scaffold, LLM protocol, Claude adapter, firm stub, config, smoke tests.

### Phase 2: Skill storage ✅ DONE
- SQLite via SQLModel
- Three tables: `skills`, `skill_versions` (history), `skill_files` (attached docs/code)
- CRUD: create_skill, update_skill, list_skills, get_skill_by_id,
  add_skill_file, get_skill_files, list_skill_versions
- Each skill folder has a `skill.json` manifest — seed script auto-discovers
  all skills under skills/ with no hardcoding required
- Seeded 3 sample skills: Skill Builder, NDA Summariser, Firm Wiki Search
- MCP factory (core/mcp/factory.py) added to match LLM and executor factory pattern

### Phase 3: Basic skill execution ✅ DONE
- Wire executor to run a skill from the DB by ID
- CLI runner: `python -m scripts.run_skill --id 1 --message "..."`
- `scripts/list_skills.py` — prints all skills from DB
- Tool registration from skill frontmatter before execution

### Phase 4: Web UI (Streamlit) ✅ DONE
- Multi-page Streamlit app (app.py)
- **Library page** (pages/1_library.py): table of skills with Run, Edit, Delete buttons
- **Create page** (pages/2_create.py): chat UI for skill creation
- **Run page** (pages/3_run.py): chat UI that loads a selected skill and lets
  the user interact with it via the executor
- User picker in sidebar (dropdown of fake users — no real auth for the demo)
- `shared.py` holds FAKE_USERS to avoid circular imports across pages

### Phase 5: Skill creation flow (the headline feature) ✅ DONE
- The Create page uses the skill-builder skill (see skills/skill-builder/SKILL.md)
  as the system prompt
- The skill-builder walks the user through an 8-stage interview:
  Purpose → Trigger → Steps → Inputs/Attachments → Tools → Output →
  Edge Cases → Name & Description
- Stage 5 prompts user to attach tools from the sidebar and asks for usage instructions
- When the LLM outputs a final SKILL.md draft, parse it out and show a preview
- "Save" writes skill + attached files to the DB
- File attachments: PDF, Excel, code, docs uploadable at creation (reference files)
  and at runtime (documents to process) — extracted to plain text via core/files.py
- Tool picker in sidebar: checkboxes for each tool in TOOL_REGISTRY; selected tools
  are injected into the interview context and written to skill frontmatter

### Phase 6: Tool execution + MCP ✅ DONE
- Skills declare tools in frontmatter: `tools: [search_wiki, lookup_contract]`
- `core/mcp/demo_tools.py` — TOOL_REGISTRY with fake implementations + `register_skill_tools()` helper
- NDA Summariser wired to `lookup_contract` (fake contract history DB)
- Firm Wiki Search wired to `search_wiki` (fake policy DB)
- Run page and CLI both auto-register tools from skill frontmatter before execution
- When firm provides real MCP servers, swap factory to RemoteMCPClient — nothing else changes

### Phase 7: Update flow + versioning ✅ DONE
- **Edit button** on Library page: opens Create page pre-loaded with existing skill content,
  tool checkboxes pre-checked, existing attached files loaded and removable
- Save in edit mode calls `update_skill()` — archives old content to `skill_versions`,
  increments version number, replaces attached files with current pending list
- **Delete button** on Library page: two-click confirmation, removes skill and all
  related SkillVersion and SkillFile records
- New CRUD: `delete_skill()`, `delete_skill_files()`

### Phase 8: Polish + demo prep ✅ DONE
- 4 polished sample skills: NDA Summariser, Firm Wiki Search, Meeting Notes
  Formatter, Expense Report Helper — all auto-seeded on startup
- Loading spinners on Create page (while LLM thinks) and Run page (while
  executor runs)
- Record backup demo video (manual — screen record the demo flow)
- 3-4 pitch slides: problem, solution, architecture, live demo

## Demo script (for the hackathon presentation)

Two-persona flow in 3-5 minutes:
1. **Tyrion (legal, non-technical)** opens the app, types "I want to create a
   skill that drafts NDA review summaries." The skill-builder interview kicks
   in, walks her through questions, produces a working skill. She attaches a
   clause guide PDF and selects the `lookup_contract` tool.
2. **Jamie (sales)** opens the library, finds Tyrion's NDA skill, clicks "Run",
   uploads an NDA PDF, gets a structured summary enriched with contract history.
3. **Bonus beat**: show the NDA skill calling `lookup_contract` to check
   counterparty history and surface a prior dispute note.

Pitch line: "GitHub for skills, but with a no-code builder."

## Important files

- `skills/skill-builder/SKILL.md` — the meta-skill that powers the Create page.
  This is the guided interview that helps users build new skills. Read it to
  understand the creation flow.
- `core/mcp/demo_tools.py` — all fake tool implementations. Add new demo tools here.
- `config.yaml` — provider selection. Change `llm.provider` to swap LLM.
- `core/llm/firm_internal.py` — stub with TODO comments showing where to wire
  the firm's API. The comments include a full reference implementation for
  OpenAI-compatible gateways.
- `shared.py` — FAKE_USERS list. Update personas here for the demo.

## Commands

```bash
# Smoke test LLM connection
python -m scripts.smoke_test_llm

# Create DB tables and seed sample skills
python -m scripts.seed_db

# List all skills in the DB
python -m scripts.list_skills

# Run a skill from the DB by ID
python -m scripts.run_skill --id 1 --message "Summarise this NDA: ..."

# Run built-in sample skill (no DB needed)
python -m scripts.run_skill

# Launch Streamlit app
streamlit run app.py
```

## Tech stack

- Python 3.11+
- Streamlit (UI)
- SQLModel + SQLite (storage)
- Anthropic SDK (current LLM, swappable)
- Pydantic (types)
- PyYAML (config)
- pdfplumber (PDF text extraction)
- openpyxl (Excel text extraction)
