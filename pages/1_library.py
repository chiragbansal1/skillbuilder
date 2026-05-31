"""
Library page — browse all skills and launch them.
"""
import streamlit as st
from core.storage.database import get_session
from core.storage.crud import list_skills

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
    st.warning("No skills found. Ask an admin to seed the database.")
    st.stop()

st.divider()

for skill in skills:
    with st.container():
        col_info, col_run = st.columns([5, 1])
        with col_info:
            st.markdown(f"### {skill.name}")
            st.caption(f"by {skill.author} · version {skill.version}")
            st.write(skill.description)
        with col_run:
            st.write("")  # vertical alignment nudge
            st.write("")
            if st.button("▶ Run", key=f"run_{skill.id}", use_container_width=True):
                st.session_state["run_skill_id"] = skill.id
                st.session_state["run_skill_name"] = skill.name
                st.switch_page("pages/3_run.py")
        st.divider()
