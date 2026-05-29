# SkillForge

Hackathon scaffold for the firm-wide skill builder. Today it runs on Claude API
locally; tomorrow it runs on the firm's LLM gateway. Zero code changes — only
config.

## Quickstart

```bash
pip install -r requirements.txt
cp .env.example .env             # add your ANTHROPIC_API_KEY
python -m scripts.smoke_test_llm # confirm the LLM connection works
python -m scripts.run_skill      # confirm a skill + tool runs end-to-end
```

## Architecture

Three pluggable layers, each behind a Protocol:

```
LLMClient        — wraps a chat-completion API (Claude today, firm tomorrow)
MCPClient        — provides tools (local stubs today, MCP servers tomorrow)
AgentExecutor    — orchestrates skill + LLM + tool-use loop
```

Anything provider-specific lives inside one adapter file. Everything else
talks only to protocols, so it has no idea which provider is in use.

```
skillforge/
├── core/
│   ├── types.py              # Provider-agnostic Message, ToolCall, LLMResponse
│   ├── llm/
│   │   ├── base.py           # LLMClient Protocol
│   │   ├── claude.py         # Anthropic SDK adapter (live)
│   │   ├── firm_internal.py  # Firm gateway adapter (stub, fill in later)
│   │   └── factory.py
│   ├── executor/
│   │   ├── base.py           # AgentExecutor Protocol + Event
│   │   ├── generic.py        # LLM-agnostic tool-use loop
│   │   └── factory.py
│   └── mcp/
│       ├── base.py           # MCPClient Protocol
│       └── local_tools.py    # In-memory Python tools (no MCP server needed)
├── scripts/
│   ├── smoke_test_llm.py
│   └── run_skill.py
├── config.yaml               # Provider selection
└── .env.example
```

## Swap LLM provider (Claude → firm gateway)

When you can talk to the firm's API:

1. Open `core/llm/firm_internal.py` — `chat()` has TODO comments with a
   reference implementation in the docstring
2. Set credentials in `.env`: `FIRM_LLM_API_KEY`, `FIRM_LLM_BASE_URL`
3. In `config.yaml`, change `llm.provider` from `claude` to `firm_internal`

Run `python -m scripts.smoke_test_llm` again — it should still pass.

## Swap MCP provider (local tools → real MCP servers)

`LocalToolsClient` lets you register Python functions as tools without running
a real MCP server — perfect for development.

For real MCP later:
1. Create `core/mcp/remote.py` implementing the `MCPClient` protocol using the
   `mcp` Python SDK (uncomment in requirements.txt)
2. Update the factory and `config.yaml`

The executor and UI don't change.

## Design rules

- **No provider SDKs outside of adapter files.** `anthropic` is imported only
  in `core/llm/claude.py`. If you find yourself importing it elsewhere,
  something has leaked.
- **Translate at the boundary.** Each adapter accepts the generic types and
  converts to/from its native format internally.
- **Tools use OpenAI-style schemas internally.** It's the most portable format.
  Adapters convert when needed (see `ClaudeClient._to_anthropic_tools`).

## What's next

Beyond Phase 0-1 (this scaffold), see the project plan for:
- Phase 2: SQLite skill storage
- Phase 3: Wire the executor to the Streamlit UI
- Phase 4: Skill creation page (chat with the skill-builder skill)
- Phase 5: Skill library + run page
- Phase 6: Add real MCP servers
