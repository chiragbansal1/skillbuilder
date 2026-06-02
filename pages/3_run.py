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
from core.mcp.demo_tools import register_skill_tools
from core.ui import render_sidebar

st.set_page_config(page_title="Run — SkillForge", page_icon="▶", layout="wide")

# Render premium custom sidebar (navigation and GPT selector)
render_sidebar("run")


# ── Helpers & Loading ────────────────────────────────────────────────────────

def load_all_skills():
    session = get_session()
    try:
        return list_skills(session, include_hidden=False)
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


# ── Skill selection logic ───────────────────────────────────────────────────

all_skills = load_all_skills()

if not all_skills:
    st.markdown("<h1 class='main-header'>▶ Run Persona</h1>", unsafe_allow_html=True)
    st.warning("No skills in the library yet. Go to Create to build one.")
    st.stop()

# Ensure we have a valid active skill in session state
if "run_skill_id" not in st.session_state or not any(s.id == st.session_state["run_skill_id"] for s in all_skills):
    # Default to the first skill
    st.session_state["run_skill_id"] = all_skills[0].id
    st.session_state["run_skill_name"] = all_skills[0].name

selected_skill_id = st.session_state["run_skill_id"]
selected_skill = next((s for s in all_skills if s.id == selected_skill_id), all_skills[0])

# Reset chat history if switching active persona
if st.session_state.get("_active_skill_id") != selected_skill.id:
    st.session_state["_active_skill_id"] = selected_skill.id
    st.session_state.pop("run_messages", None)

# Avatar Initials
words = selected_skill.name.split()
initials = "".join([w[0].upper() for w in words[:2]])

# Render Active Persona Header
st.markdown(
    f"""
    <div class="glass-card" style="display: flex; align-items: center; margin-bottom: 2rem; padding: 1.2rem !important;">
        <div class="persona-avatar" style="margin-right: 1.25rem;">
            {initials}
        </div>
        <div>
            <h4 style="margin: 0;">{selected_skill.name}</h4>
            <p style="margin: 0.2rem 0 0 0;">{selected_skill.description} • Created by <b>{selected_skill.author}</b></p>
        </div>
    </div>
    """,
    unsafe_allow_html=True
)


# ── Executor setup ───────────────────────────────────────────────────────────

provider = st.session_state.get("llm_provider", "gemini")
key = st.session_state.get("gemini_api_key" if provider == "gemini" else "anthropic_api_key", "")
model = "gemini-2.5-flash" if provider == "gemini" else "claude-opus-4-7"

try:
    llm = make_llm_client()
    mcp = make_mcp_client()
    executor = make_executor(llm=llm, mcp=mcp)
except Exception as e:
    st.error(f"Could not initialise the AI engine: {e}")
    st.stop()


# ── Chat UI ──────────────────────────────────────────────────────────────────

st.session_state.setdefault("run_messages", [])

# Auto-generate welcome greeting if chat is empty (skill just loaded)
if not st.session_state["run_messages"]:
    skill_content = load_skill_content(selected_skill.id)
    register_skill_tools(mcp, skill_content)
    with st.spinner("Loading persona…"):
        try:
            from core.types import Message
            greeting_prompt = (
                "Introduce yourself briefly in 2-3 sentences based on your skill description. "
                "Tell the user what you can help with and give 2-3 example prompts they can try. "
                "Be concise and professional."
            )
            response = llm.chat(
                messages=[Message(role="user", content=greeting_prompt)],
                system=skill_content,
            )
            welcome = response.content or f"Hi! I'm **{selected_skill.name}**. How can I help you today?"
        except Exception:
            welcome = f"Hi! I'm **{selected_skill.name}**. {selected_skill.description}. How can I help you today?"
    st.session_state["run_messages"] = [{"role": "assistant", "content": welcome, "tool_logs": []}]
    st.rerun()


# Display existing chat messages
for msg in st.session_state["run_messages"]:
    with st.chat_message(msg["role"]):
        if "tool_logs" in msg and msg["tool_logs"]:
            for log in msg["tool_logs"]:
                st.markdown(log, unsafe_allow_html=True)
        st.markdown(msg["content"])

# File attachment interface
with st.expander("📎 Attach reference files to this prompt", expanded=False):
    st.caption("Upload documents, CSVs, or code. The AI persona will read and include them as context.")
    run_uploads = st.file_uploader(
        "Upload files",
        accept_multiple_files=True,
        type=["py", "md", "txt", "json", "yaml", "csv", "pdf", "xlsx", "xls"],
        key=f"run_uploader_{selected_skill.id}",
        label_visibility="collapsed",
    )

# Prompt input
user_input = st.chat_input(f"Message {selected_skill.name}…")

if user_input:
    # Build message with attached file contexts
    full_user_message = user_input
    display_user_message = user_input

    if run_uploads:
        file_sections = []
        file_labels = []
        for uf in run_uploads:
            text = extract_text(uf.name, uf.read())
            file_sections.append(f"\n\n---\n**Attached File Context: {uf.name}**\n\n{text}")
            file_labels.append(uf.name)
        full_user_message += "".join(file_sections)
        display_user_message += f"\n\n*📎 Attached: {', '.join(file_labels)}*"

    # Display user message
    st.session_state["run_messages"].append({"role": "user", "content": display_user_message})
    with st.chat_message("user"):
        st.markdown(display_user_message)

    # Load prompt template and register skill tools
    skill_content = load_skill_content(selected_skill.id)
    registered = register_skill_tools(mcp, skill_content)

    # Streaming assistant response
    with st.chat_message("assistant"):
        tool_log = st.container()
        response_placeholder = st.empty()
        full_response = ""
        current_tool_logs = []

        try:
            with st.spinner("Processing analysis…"):
                prior = st.session_state["run_messages"][:-1]  # Exclude user's latest prompt
                for event in executor.run(skill_content=skill_content, user_message=full_user_message, history=prior):
                    if event.type == "text":
                        full_response += event.data["text"]
                        response_placeholder.markdown(full_response + "▌")
                    elif event.type == "tool_call":
                        log_html = f"<span class='custom-badge badge-primary'>🔧 Calling: {event.data['name']}</span>"
                        tool_log.markdown(log_html, unsafe_allow_html=True)
                        current_tool_logs.append(log_html)
                    elif event.type == "tool_result":
                        pass
                    elif event.type == "error":
                        st.error(event.data.get("message", "Execution error"))

            response_placeholder.markdown(full_response)
        except Exception as e:
            full_response = f"Sorry, an error occurred during execution: {e}"
            response_placeholder.markdown(full_response)

    st.session_state["run_messages"].append({
        "role": "assistant", 
        "content": full_response,
        "tool_logs": current_tool_logs
    })
    st.rerun()
