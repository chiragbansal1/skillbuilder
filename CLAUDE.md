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

### Phase 2: Skill storage (next)
- SQLite via SQLModel
- `skills` table: id, name, description, content (SKILL.md text), author,
  version, created_at, updated_at
- `skill_versions` table for history
- CRUD: create_skill, update_skill, list_skills, get_skill_by_id
- Seed with 2-3 sample skills including the skill-builder skill itself

### Phase 3: Basic skill execution
- Wire executor to run a skill from the DB by ID
- CLI runner: `python -m scripts.run_skill --id 1 --message "..."`
- Confirm end-to-end on a simple skill (no tools)

### Phase 4: Web UI (Streamlit)
- Multi-page Streamlit app (app.py)
- **Library page** (pages/1_library.py): table of skills, "Run" and "Edit" buttons
- **Create page** (pages/2_create.py): chat UI for skill creation
- **Run page** (pages/3_run.py): chat UI that loads a selected skill and lets
  the user interact with it via the executor
- User picker in sidebar (dropdown of fake users — no real auth for the demo)

### Phase 5: Skill creation flow (the headline feature)
- The Create page uses the skill-builder skill (see skills/skill-builder/SKILL.md)
  as the system prompt
- The skill-builder walks the user through an 8-stage interview:
  Purpose → Trigger → Steps → Inputs/Attachments → Tools → Output →
  Edge Cases → Name & Description
- When the LLM outputs a final SKILL.md draft, parse it out and show a preview
- "Save" writes to the DB. "Test" runs the skill with a sample prompt.
- User can also paste existing skill content to update it (update mode)

### Phase 6: Tool execution + MCP
- Skills can declare required MCP servers in their frontmatter:
  ```yaml
  mcp_servers:
    - name: contracts_db
      url: https://internal-mcp.yourfirm.com/contracts
  ```
- The executor passes these to the MCP client
- For the demo: create at least one fake MCP server (e.g., a "firm wiki search")
  using LocalToolsClient
- When firm provides real MCP servers, swap to RemoteMCPClient

### Phase 7: Update flow + versioning
- "Edit" button on library page opens a chat pre-loaded with the existing skill
- Save increments version, writes to skill_versions
- Optional: show diff between versions

### Phase 8: Polish + demo prep
- Seed 3-4 polished sample skills (NDA summariser, meeting notes formatter,
  internal wiki search, expense report helper)
- Loading states, error handling
- Record backup demo video
- 3-4 pitch slides: problem, solution, architecture, live demo

## Demo script (for the hackathon presentation)

Two-persona flow in 3-5 minutes:
1. **Priya (legal, non-technical)** opens the app, types "I want to create a
   skill that drafts NDA review summaries." The skill-builder interview kicks
   in, walks her through questions, and produces a working skill.
2. **Raj (sales)** opens the library, finds Priya's NDA skill, clicks "Run",
   uploads an NDA, gets a structured summary.
3. **Bonus beat**: show the NDA skill calling an MCP tool (firm contract
   database) to enrich the summary.

Pitch line: "GitHub for skills, but with a no-code builder."

## Important files

- `skills/skill-builder/SKILL.md` — the meta-skill that powers the Create page.
  This is the guided interview that helps users build new skills. Read it to
  understand the creation flow.
- `config.yaml` — provider selection. Change `llm.provider` to swap LLM.
- `core/llm/firm_internal.py` — stub with TODO comments showing where to wire
  the firm's API. The comments include a full reference implementation for
  OpenAI-compatible gateways.

## Commands

```bash
# Smoke test LLM connection
python -m scripts.smoke_test_llm

# Run a sample skill end-to-end (with tool call)
python -m scripts.run_skill

# Launch Streamlit app (after Phase 4)
streamlit run app.py
```

## Tech stack

- Python 3.11+
- Streamlit (UI)
- SQLModel + SQLite (storage)
- Anthropic SDK (current LLM, swappable)
- Pydantic (types)
- PyYAML (config)
