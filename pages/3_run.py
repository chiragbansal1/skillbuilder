"""
Run page — chat UI that loads a skill from the DB and runs it via the executor.
"""
import streamlit as st
from dotenv import load_dotenv
load_dotenv()

from core.llm.factory import make_llm_client
from core.mcp.factory import make_mcp_client
from core.executor.factory import make_executor
from core.storage.database import get_session
from core.storage.crud import get_skill_by_id, get_skill_files, list_skills
from core.files import extract_text

st.set_page_config(page_title="Run — SkillForge", page_icon="▶", layout="wide")

with st.sidebar:
    st.title("⚡ SkillForge")
    st.divider()
    from shared import FAKE_USERS
    st.session_state.setdefault("current_user", FAKE_USERS[0])
    st.session_state["current_user"] = st.selectbox(
        "Signed in as",
        FAKE_USERS,
        index=FAKE_USERS.index(st.session_state["current_user"]),
    )
    st.divider()
    if st.button("🗑 Clear chat", use_container_width=True):
        st.session_state.pop("run_messages", None)
        st.rerun()


# ── Skill selector ──────────────────────────────────────────────────────────

def load_all_skills():
    session = get_session()
    try:
        return list_skills(session)
    finally:
        session.close()


def load_skill_content(skill_id: int) -> str:
    session = get_session()
    try:
        skill = get_skill_by_id(session, skill_id)
        if not skill:
            return ""
        content = skill.content
        files = get_skill_files(session, skill_id)
        if files:
            content += "\n\n---\n## Attached reference files\n"
            for f in files:
                content += f"\n### {f.filename}\n{f.content}\n"
        return content
    finally:
        session.close()


all_skills = load_all_skills()

if not all_skills:
    st.title("▶ Run a Skill")
    st.warning("No skills in the library yet. Ask an admin to seed the database.")
    st.stop()

skill_map = {f"{s.name} (id={s.id})": s for s in all_skills}

# Pre-select from library page navigation if available
default_label = None
if "run_skill_id" in st.session_state:
    for label, s in skill_map.items():
        if s.id == st.session_state["run_skill_id"]:
            default_label = label
            break

selected_label = st.selectbox(
    "Choose a skill to run",
    list(skill_map.keys()),
    index=list(skill_map.keys()).index(default_label) if default_label else 0,
)
selected_skill = skill_map[selected_label]

# Reset chat when skill changes
if st.session_state.get("_active_skill_id") != selected_skill.id:
    st.session_state["_active_skill_id"] = selected_skill.id
    st.session_state.pop("run_messages", None)

st.title(f"▶ {selected_skill.name}")
st.caption(selected_skill.description)
st.divider()


# ── Executor (cached per skill) ──────────────────────────────────────────────

@st.cache_resource
def get_executor():
    llm = make_llm_client()
    mcp = make_mcp_client()
    return make_executor(llm=llm, mcp=mcp)


try:
    executor = get_executor()
except Exception as e:
    st.error(f"Could not initialise the AI engine: {e}")
    st.info("Make sure your `.env` file contains a valid `ANTHROPIC_API_KEY`.")
    st.stop()


# ── Chat UI ──────────────────────────────────────────────────────────────────

st.session_state.setdefault("run_messages", [])

for msg in st.session_state["run_messages"]:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# File upload — sits above the chat input
with st.expander("📎 Attach files to your message", expanded=False):
    st.caption("Upload documents, code, PDFs, or spreadsheets to include with your next message.")
    run_uploads = st.file_uploader(
        "Upload files",
        accept_multiple_files=True,
        type=["py", "md", "txt", "json", "yaml", "csv", "pdf", "xlsx", "xls"],
        key=f"run_uploader_{selected_skill.id}",
        label_visibility="collapsed",
    )

user_input = st.chat_input(f"Ask {selected_skill.name} something…")

if user_input:
    # Build message: text + any uploaded file contents
    full_user_message = user_input
    display_user_message = user_input

    if run_uploads:
        file_sections = []
        file_labels = []
        for uf in run_uploads:
            text = extract_text(uf.name, uf.read())
            file_sections.append(f"\n\n---\n**File: {uf.name}**\n\n{text}")
            file_labels.append(uf.name)
        full_user_message += "".join(file_sections)
        display_user_message += f"\n\n*Attached: {', '.join(file_labels)}*"

    st.session_state["run_messages"].append({"role": "user", "content": display_user_message})
    with st.chat_message("user"):
        st.markdown(display_user_message)

    skill_content = load_skill_content(selected_skill.id)

    with st.chat_message("assistant"):
        response_placeholder = st.empty()
        tool_log = st.container()
        full_response = ""

        try:
            for event in executor.run(skill_content=skill_content, user_message=full_user_message):
                if event.type == "text":
                    full_response += event.data["text"]
                    response_placeholder.markdown(full_response + "▌")
                elif event.type == "tool_call":
                    tool_log.caption(f"🔧 Calling `{event.data['name']}`…")
                elif event.type == "tool_result":
                    tool_log.caption(f"↩ Tool returned: {str(event.data['content'])[:120]}")
                elif event.type == "error":
                    st.error(event.data.get("message", "Unknown error"))

            response_placeholder.markdown(full_response)
        except Exception as e:
            full_response = f"Something went wrong: {e}"
            response_placeholder.markdown(full_response)

    st.session_state["run_messages"].append({"role": "assistant", "content": full_response})
