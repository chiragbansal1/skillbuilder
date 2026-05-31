"""
Library page — browse, run, edit, and delete skills.
"""
import streamlit as st
from core.storage.database import get_session
from core.storage.crud import list_skills, delete_skill

st.set_page_config(page_title="Library — SkillForge", page_icon="📚", layout="wide")

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

st.title("📚 Skill Library")
st.caption("Browse and run skills built by your colleagues.")

session = get_session()
try:
    skills = list_skills(session)
finally:
    session.close()

if not skills:
    st.info("No skills yet — go to **Create** to build the first one.")
    st.stop()

st.divider()

for skill in skills:
    with st.container():
        col_info, col_run, col_edit, col_delete = st.columns([5, 1, 1, 1])

        with col_info:
            st.markdown(f"### {skill.name}")
            st.caption(f"by {skill.author} · version {skill.version}")
            st.write(skill.description)

        with col_run:
            st.write("")
            st.write("")
            if st.button("▶ Run", key=f"run_{skill.id}", use_container_width=True):
                st.session_state["run_skill_id"] = skill.id
                st.session_state["run_skill_name"] = skill.name
                st.switch_page("pages/3_run.py")

        with col_edit:
            st.write("")
            st.write("")
            if st.button("✏️ Edit", key=f"edit_{skill.id}", use_container_width=True):
                # Clear any previous create/edit session state
                for key in ["create_messages", "create_llm_messages", "create_draft",
                            "create_saved_id", "create_pending_files", "create_testing"]:
                    st.session_state.pop(key, None)
                st.session_state["edit_skill_id"] = skill.id
                st.switch_page("pages/2_create.py")

        with col_delete:
            st.write("")
            st.write("")
            if st.session_state.get(f"confirm_delete_{skill.id}"):
                if st.button("Sure?", key=f"confirm_{skill.id}", use_container_width=True, type="primary"):
                    session = get_session()
                    try:
                        delete_skill(session, skill.id)
                    finally:
                        session.close()
                    st.session_state.pop(f"confirm_delete_{skill.id}", None)
                    st.rerun()
            else:
                if st.button("🗑 Delete", key=f"delete_{skill.id}", use_container_width=True):
                    st.session_state[f"confirm_delete_{skill.id}"] = True
                    st.rerun()

        st.divider()
