"""
Create page — guided skill-builder interview.

Uses the skill-builder SKILL.md as the system prompt to conduct an 8-stage
interview, parses the final SKILL.md draft, and lets the user save or test it.
"""
import re
import yaml
import streamlit as st
from pathlib import Path
from dotenv import load_dotenv
load_dotenv()

from shared import FAKE_USERS
from core.llm.factory import make_llm_client
from core.mcp.factory import make_mcp_client
from core.executor.factory import make_executor
from core.types import Message
from core.storage.database import get_session
from core.storage.crud import create_skill, add_skill_file, get_skill_by_id, get_skill_files, update_skill, delete_skill_files
from core.files import extract_text, file_type_label
from core.mcp.demo_tools import register_skill_tools, TOOL_REGISTRY

# ── Page config & sidebar ────────────────────────────────────────────────────

st.set_page_config(page_title="Create — SkillForge", page_icon="✨", layout="wide")

with st.sidebar:
    st.title("⚡ SkillForge")
    st.divider()
    st.session_state.setdefault("current_user", FAKE_USERS[0])
    st.session_state["current_user"] = st.selectbox(
        "Signed in as",
        FAKE_USERS,
        index=FAKE_USERS.index(st.session_state["current_user"]),
    )
    st.divider()
    st.markdown("**🔧 Attach tools**")
    st.caption("Select tools this skill should be able to call. You can tell the AI any specific instructions for each tool during the interview.")
    for tool_name, tool in TOOL_REGISTRY.items():
        st.checkbox(
            tool_name,
            help=tool["description"],
            key=f"create_tool_{tool_name}",
        )
    st.divider()
    st.markdown("**📎 Attach reference files**")
    st.caption("Upload docs, code, or data the skill should know about.")
    sidebar_uploads = st.file_uploader(
        "Attach files",
        accept_multiple_files=True,
        type=["py", "md", "txt", "json", "yaml", "csv", "pdf", "xlsx", "xls"],
        key="create_sidebar_uploader",
        label_visibility="collapsed",
    )
    if sidebar_uploads:
        existing_names = {f["filename"] for f in st.session_state.get("create_pending_files", [])}
        for uf in sidebar_uploads:
            if uf.name not in existing_names:
                from core.files import extract_text, file_type_label
                text = extract_text(uf.name, uf.read())
                st.session_state["create_pending_files"].append({
                    "filename": uf.name,
                    "file_type": file_type_label(uf.name),
                    "content": text,
                })
                existing_names.add(uf.name)
    if st.session_state.get("create_pending_files"):
        for f in st.session_state["create_pending_files"]:
            st.caption(f"📎 {f['filename']}")
    st.divider()
    if st.button("🗑 Start over", use_container_width=True):
        for key in ["create_messages", "create_llm_messages", "create_draft",
                    "create_saved_id", "create_pending_files", "create_testing",
                    "edit_skill_id"]:
            st.session_state.pop(key, None)
        st.rerun()


# ── Helpers ──────────────────────────────────────────────────────────────────

SKILL_BUILDER_PATH = Path("skills/skill-builder/SKILL.md")
OPENING_MESSAGE = (
    "Hi! I'm here to help you build a new skill. "
    "To get started, tell me: **what do you want this skill to do?**\n\n"
    "For example: *\"I want a skill that summarises NDA documents\"* or "
    "*\"I need something that formats meeting notes.\"*"
)


@st.cache_resource
def get_llm():
    return make_llm_client()


@st.cache_resource
def get_executor_stack():
    llm = make_llm_client()
    mcp = make_mcp_client()
    executor = make_executor(llm=llm, mcp=mcp)
    return executor, mcp


def load_skill_builder_prompt() -> str:
    return SKILL_BUILDER_PATH.read_text(encoding="utf-8")


def parse_skill_draft(text: str) -> str | None:
    """Return content inside ```skill ... ``` block, or None."""
    match = re.search(r"```skill\n(.*?)```", text, re.DOTALL)
    return match.group(1).strip() if match else None


def extract_frontmatter(skill_content: str) -> dict:
    """Parse YAML frontmatter from a skill string."""
    match = re.match(r"^---\n(.*?)\n---", skill_content, re.DOTALL)
    if match:
        try:
            return yaml.safe_load(match.group(1)) or {}
        except yaml.YAMLError:
            pass
    return {}


def save_skill_to_db(skill_content: str, author: str, pending_files: list[dict]) -> int:
    meta = extract_frontmatter(skill_content)
    name = meta.get("name", "Untitled Skill")
    description = meta.get("description", "")
    session = get_session()
    try:
        skill = create_skill(
            session=session,
            name=name,
            description=description,
            content=skill_content,
            author=author,
        )
        for f in pending_files:
            add_skill_file(
                session=session,
                skill_id=skill.id,
                filename=f["filename"],
                file_type=f["file_type"],
                content=f["content"],
            )
        return skill.id
    finally:
        session.close()


def update_skill_in_db(skill_id: int, skill_content: str, pending_files: list[dict]) -> int:
    session = get_session()
    try:
        skill = update_skill(session=session, skill_id=skill_id, content=skill_content)
        # Replace all attached files with the current pending list
        delete_skill_files(session=session, skill_id=skill_id)
        for f in pending_files:
            add_skill_file(
                session=session,
                skill_id=skill_id,
                filename=f["filename"],
                file_type=f["file_type"],
                content=f["content"],
            )
        return skill.version
    finally:
        session.close()


def run_test(skill_content: str, test_message: str):
    """Yield events from a quick test run of the drafted skill."""
    executor, mcp = get_executor_stack()
    register_skill_tools(mcp, skill_content)
    yield from executor.run(skill_content=skill_content, user_message=test_message)


# ── Session state defaults ────────────────────────────────────────────────────

st.session_state.setdefault("create_messages", [
    {"role": "assistant", "content": OPENING_MESSAGE}
])
st.session_state.setdefault("create_llm_messages", [])
st.session_state.setdefault("create_draft", None)
st.session_state.setdefault("create_saved_id", None)
st.session_state.setdefault("create_pending_files", [])

# ── Edit mode — pre-load existing skill ──────────────────────────────────────

edit_skill_id = st.session_state.get("edit_skill_id")

if edit_skill_id and st.session_state["create_draft"] is None:
    session = get_session()
    try:
        existing = get_skill_by_id(session, edit_skill_id)
        existing_files = get_skill_files(session, edit_skill_id) if existing else []
    finally:
        session.close()

    if existing:
        edit_opening = (
            f"You're editing **{existing.name}** (version {existing.version}). "
            f"The current skill is shown on the right.\n\n"
            f"Tell me what you'd like to change — I'll update the skill and show you a new draft."
        )
        st.session_state["create_messages"] = [{"role": "assistant", "content": edit_opening}]
        st.session_state["create_llm_messages"] = [{
            "role": "assistant",
            "content": (
                f"The user wants to edit an existing skill. Here is the current SKILL.md:\n\n"
                f"```skill\n{existing.content}\n```\n\n"
                f"Ask them what they'd like to change."
            ),
        }]
        st.session_state["create_draft"] = existing.content

        # Pre-load existing attached files so user can review/remove them
        st.session_state["create_pending_files"] = [
            {"filename": f.filename, "file_type": f.file_type, "content": f.content}
            for f in existing_files
        ]

        # Pre-check tool checkboxes based on existing frontmatter
        meta = extract_frontmatter(existing.content)
        for tool_name in meta.get("tools", []):
            st.session_state[f"create_tool_{tool_name}"] = True


# ── Layout ────────────────────────────────────────────────────────────────────

is_edit_mode = bool(edit_skill_id)

if is_edit_mode:
    col_title, col_new = st.columns([5, 2])
    with col_title:
        st.title("✏️ Edit Skill")
        st.caption("Update the skill using the chat below.")
    with col_new:
        st.write("")
        if st.button("✨ Start new skill instead", use_container_width=True):
            for key in ["create_messages", "create_llm_messages", "create_draft",
                        "create_saved_id", "create_pending_files", "edit_skill_id"]:
                st.session_state.pop(key, None)
            st.rerun()
else:
    st.title("✨ Create a Skill")
    st.caption("Answer a few questions and the AI will write the skill for you.")

draft = st.session_state["create_draft"]

if draft:
    chat_col, preview_col = st.columns([3, 2], gap="large")
else:
    chat_col = st.container()
    preview_col = None


# ── Chat panel ────────────────────────────────────────────────────────────────

with chat_col:
    for msg in st.session_state["create_messages"]:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    user_input = st.chat_input("Your answer…")

    if user_input:
        # Display user message immediately
        st.session_state["create_messages"].append({"role": "user", "content": user_input})
        with st.chat_message("user"):
            st.markdown(user_input)

        # Build LLM message history
        llm_msgs = [
            Message(role=m["role"], content=m["content"])
            for m in st.session_state["create_llm_messages"]
        ]

        # Append selected tools so the LLM includes them in the frontmatter
        selected_tools = [
            name for name in TOOL_REGISTRY
            if st.session_state.get(f"create_tool_{name}")
        ]
        msg_content = user_input
        if selected_tools:
            msg_content += (
                f"\n\n[System note: the user has selected these tools for this skill: "
                f"{', '.join(selected_tools)}. Include them in the skill frontmatter as:\n"
                f"tools:\n" + "".join(f"  - {t}\n" for t in selected_tools) + "]"
            )
        llm_msgs.append(Message(role="user", content=msg_content))

        # Call LLM
        with st.spinner("Thinking…"):
            try:
                llm = get_llm()
                system_prompt = load_skill_builder_prompt()
                response = llm.chat(messages=llm_msgs, system=system_prompt)
                reply = response.content
            except Exception as e:
                reply = f"Sorry, I couldn't reach the AI: {e}\n\nMake sure your `.env` has a valid `ANTHROPIC_API_KEY`."

        # Persist messages
        st.session_state["create_llm_messages"].append({"role": "user", "content": user_input})
        st.session_state["create_llm_messages"].append({"role": "assistant", "content": reply})
        st.session_state["create_messages"].append({"role": "assistant", "content": reply})

        # Check for a completed skill draft
        new_draft = parse_skill_draft(reply)
        if new_draft:
            st.session_state["create_draft"] = new_draft
            st.session_state["create_saved_id"] = None

        with st.chat_message("assistant"):
            st.markdown(reply)

        st.rerun()


# ── Preview panel ─────────────────────────────────────────────────────────────

if draft and preview_col:
    with preview_col:
        meta = extract_frontmatter(draft)
        skill_name = meta.get("name", "New Skill")

        st.subheader(f"📄 {skill_name}")
        st.caption(meta.get("description", ""))
        st.divider()

        with st.expander("View full SKILL.md", expanded=True):
            st.code(draft, language="markdown")

        # ── Reference file upload ─────────────────────────────────────────
        st.markdown("**Attach reference files** *(optional)*")
        st.caption("Add docs, code, or data the skill should know about — e.g. clause guides, templates, pricing sheets.")

        uploaded = st.file_uploader(
            "Upload files",
            accept_multiple_files=True,
            type=["py", "md", "txt", "json", "yaml", "csv", "pdf", "xlsx", "xls"],
            key="create_uploader",
            label_visibility="collapsed",
        )

        if uploaded:
            existing_names = {f["filename"] for f in st.session_state["create_pending_files"]}
            for uf in uploaded:
                if uf.name not in existing_names:
                    text = extract_text(uf.name, uf.read())
                    st.session_state["create_pending_files"].append({
                        "filename": uf.name,
                        "file_type": file_type_label(uf.name),
                        "content": text,
                    })
                    existing_names.add(uf.name)

        pending = st.session_state["create_pending_files"]
        if pending:
            for i, f in enumerate(pending):
                c1, c2 = st.columns([5, 1])
                c1.caption(f"📎 {f['filename']} ({f['file_type']})")
                if c2.button("✕", key=f"rm_file_{i}"):
                    st.session_state["create_pending_files"].pop(i)
                    st.rerun()

        st.divider()

        saved_id = st.session_state.get("create_saved_id")

        if saved_id:
            if is_edit_mode:
                st.success(f"Updated to version {saved_id}!")
            else:
                st.success(f"Saved! Skill id={saved_id}")
            if st.button("Go to Library →", use_container_width=True):
                for key in ["create_messages", "create_llm_messages", "create_draft",
                            "create_saved_id", "create_pending_files", "edit_skill_id"]:
                    st.session_state.pop(key, None)
                st.switch_page("pages/1_library.py")
        else:
            label = "💾 Save changes" if is_edit_mode else "💾 Save skill"
            if st.button(label, use_container_width=True):
                author = st.session_state.get("current_user", "unknown")
                try:
                    if is_edit_mode:
                        new_version = update_skill_in_db(
                            edit_skill_id, draft, st.session_state["create_pending_files"]
                        )
                        st.session_state["create_saved_id"] = new_version
                    else:
                        skill_id = save_skill_to_db(
                            draft, author, st.session_state["create_pending_files"]
                        )
                        st.session_state["create_saved_id"] = skill_id
                    st.rerun()
                except Exception as e:
                    st.error(f"Save failed: {e}")
