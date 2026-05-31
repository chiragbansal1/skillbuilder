"""
SkillForge — main Streamlit entry point.

Renders the home/welcome page and the sidebar that persists across all pages.
"""
import streamlit as st
from shared import FAKE_USERS
from scripts.seed_db import seed

seed()

st.set_page_config(
    page_title="SkillForge",
    page_icon="⚡",
    layout="wide",
)

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
    st.caption("Navigate using the pages in the sidebar.")

st.title("Welcome to SkillForge")
st.subheader("GitHub for skills — with a no-code builder.")

st.markdown("""
SkillForge lets anyone at the firm create, share, and run AI-powered skills —
no coding required.

**Get started:**
- **Library** — browse and run existing skills
- **Create** — build a new skill using a guided interview
""")

col1, col2 = st.columns(2)
with col1:
    st.info("**New here?** Head to **Create** and describe what you want the skill to do. The AI will guide you through the rest.")
with col2:
    st.info("**Looking for a skill?** Open **Library** to see everything the firm has built so far.")
