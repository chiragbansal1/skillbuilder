"""
SkillForge — main Streamlit entry point.

Renders the home/welcome page and the sidebar that persists across all pages.
"""
import streamlit as st
from scripts.seed_db import seed
from core.ui import render_sidebar

# Seed database with skills
seed()

st.set_page_config(
    page_title="SkillForge — Enterprise AI Skills",
    page_icon="⚡",
    layout="wide",
)

# Render custom premium sidebar
render_sidebar("home")

# Header section
st.markdown("<h1 class='main-header'>⚡ Welcome to SkillForge</h1>", unsafe_allow_html=True)
st.markdown("<h3 style='margin-top: -1.2rem; color: #94a3b8 !important; font-weight: 400 !important; font-size: 1.25rem;'>The Collaborative AI Skill & Persona Platform for the Enterprise</h3>", unsafe_allow_html=True)
st.write("")

# Metrics Grid
c1, c2, c3, c4 = st.columns(4)
with c1:
    st.markdown(
        """
        <div class="glass-card" style="text-align: center; padding: 1rem;">
            <p style="margin: 0; font-size: 0.8rem; color: #94a3b8; font-weight: 500; text-transform: uppercase;">Active Skills</p>
            <h2 style="margin: 0.5rem 0; font-size: 2.2rem; font-weight: 700; color: #a5b4fc !important;">4</h2>
            <p style="margin: 0; font-size: 0.75rem; color: #34d399;">✔ Fully Seeded</p>
        </div>
        """,
        unsafe_allow_html=True
    )
with c2:
    st.markdown(
        """
        <div class="glass-card" style="text-align: center; padding: 1rem;">
            <p style="margin: 0; font-size: 0.8rem; color: #94a3b8; font-weight: 500; text-transform: uppercase;">Registered MCP Tools</p>
            <h2 style="margin: 0.5rem 0; font-size: 2.2rem; font-weight: 700; color: #a5b4fc !important;">93</h2>
            <p style="margin: 0; font-size: 0.75rem; color: #6366f1;">• 6 Pillars Active</p>
        </div>
        """,
        unsafe_allow_html=True
    )
with c3:
    st.markdown(
        """
        <div class="glass-card" style="text-align: center; padding: 1rem;">
            <p style="margin: 0; font-size: 0.8rem; color: #94a3b8; font-weight: 500; text-transform: uppercase;">Active Profiles</p>
            <h2 style="margin: 0.5rem 0; font-size: 2.2rem; font-weight: 700; color: #a5b4fc !important;">10</h2>
            <p style="margin: 0; font-size: 0.75rem; color: #a5b4fc;">• Role-based Access</p>
        </div>
        """,
        unsafe_allow_html=True
    )
with c4:
    import os
    is_offline = not os.environ.get("ANTHROPIC_API_KEY")
    status_color = "#fbbf24" if is_offline else "#34d399"
    status_label = "Mock Fallback (Offline)" if is_offline else "Connected (Claude 3)"
    st.markdown(
        f"""
        <div class="glass-card" style="text-align: center; padding: 1rem;">
            <p style="margin: 0; font-size: 0.8rem; color: #94a3b8; font-weight: 500; text-transform: uppercase;">AI Engine Status</p>
            <h2 style="margin: 0.5rem 0; font-size: 1.5rem; font-weight: 700; color: {status_color} !important; height: 3.3rem; display: flex; align-items: center; justify-content: center;">{status_label}</h2>
        </div>
        """,
        unsafe_allow_html=True
    )

st.write("")

# Highlighted Features Section
st.markdown("### 🛠 Get Started with SkillForge")

col1, col2, col3 = st.columns(3, gap="large")

with col1:
    st.markdown(
        """
        <div class="glass-card" style="min-height: 250px;">
            <div style="font-size: 2rem; margin-bottom: 0.5rem;">📚</div>
            <h4 style="margin: 0.25rem 0 0.75rem 0; font-size: 1.2rem;">Explore the Skill Library</h4>
            <p style="font-size: 0.85rem; color: #94a3b8; line-height: 1.5;">
                Browse the complete directory of skills built by your organization. Run pre-configured skills for contract lookup, policy Q&A, and financial analysis.
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )
    if st.button("Go to Library →", use_container_width=True):
        st.switch_page("pages/1_library.py")

with col2:
    st.markdown(
        """
        <div class="glass-card" style="min-height: 250px;">
            <div style="font-size: 2rem; margin-bottom: 0.5rem;">✨</div>
            <h4 style="margin: 0.25rem 0 0.75rem 0; font-size: 1.2rem;">Create a Skill</h4>
            <p style="font-size: 0.85rem; color: #94a3b8; line-height: 1.5;">
                Build custom agentic skills without writing code. Engage in a guided 8-stage interview with our AI Skill Builder to configure prompts, attach database tools, and save them.
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )
    if st.button("Create new Skill →", use_container_width=True):
        st.switch_page("pages/2_create.py")

with col3:
    st.markdown(
        """
        <div class="glass-card" style="min-height: 250px;">
            <div style="font-size: 2rem; margin-bottom: 0.5rem;">💬</div>
            <h4 style="margin: 0.25rem 0 0.75rem 0; font-size: 1.2rem;">Run Personas (GPTs)</h4>
            <p style="font-size: 0.85rem; color: #94a3b8; line-height: 1.5;">
                Chat with specific skills in an interface modeled after ChatGPT's custom GPTs. Dynamically select a persona from the sidebar, attach reference files, and run tasks.
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )
    if st.button("Open Run Chat →", use_container_width=True):
        st.switch_page("pages/3_run.py")

st.divider()

# Information Box
st.markdown(
    """
    <div class="glass-card" style="background: rgba(99, 102, 241, 0.05); border-color: rgba(99, 102, 241, 0.25);">
        <h4 style="margin: 0 0 0.5rem 0; color: #a5b4fc !important;">🔥 Feature Highlight: Wall Street AI Analyst Skill</h4>
        <p style="margin: 0; font-size: 0.85rem; color: #cbd5e1; line-height: 1.6;">
            We have integrated a state-of-the-art <b>Financial Modelling Suite</b> including a database of <b>50 companies</b> and <b>90 analytical tools</b>. 
            Test WACC calculations, DCF models, DuPont ROE decompositions, M&A history research, and generate investment reports instantly from the <b>Run</b> page by selecting the <b>Wall Street AI Analyst</b> persona.
        </p>
    </div>
    """,
    unsafe_allow_html=True
)
