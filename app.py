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
st.markdown("<h3 class='main-subheader'>The Collaborative AI Skill & Persona Platform for the Enterprise</h3>", unsafe_allow_html=True)
st.write("")

# Metrics Grid
c1, c2, c3, c4 = st.columns(4)
with c1:
    st.markdown(
        """
        <div class="glass-card" style="text-align: center; padding: 1.2rem; margin-bottom: 0;">
            <p style="margin: 0; font-size: 0.8rem; color: #ca8a04; font-weight: 600; text-transform: uppercase; letter-spacing: 0.05em;">Active Skills</p>
            <h2 style="margin: 0.5rem 0; font-size: 2.2rem; font-weight: 700; color: #ffffff !important;">4</h2>
            <p style="margin: 0; font-size: 0.75rem; color: #10b981;">✔ Fully Seeded</p>
        </div>
        """,
        unsafe_allow_html=True
    )
with c2:
    st.markdown(
        """
        <div class="glass-card" style="text-align: center; padding: 1.2rem; margin-bottom: 0;">
            <p style="margin: 0; font-size: 0.8rem; color: #ca8a04; font-weight: 600; text-transform: uppercase; letter-spacing: 0.05em;">MCP Tools</p>
            <h2 style="margin: 0.5rem 0; font-size: 2.2rem; font-weight: 700; color: #ffffff !important;">10</h2>
            <p style="margin: 0; font-size: 0.75rem; color: #ca8a04;">• Financial Intel</p>
        </div>
        """,
        unsafe_allow_html=True
    )
with c3:
    st.markdown(
        """
        <div class="glass-card" style="text-align: center; padding: 1.2rem; margin-bottom: 0;">
            <p style="margin: 0; font-size: 0.8rem; color: #ca8a04; font-weight: 600; text-transform: uppercase; letter-spacing: 0.05em;">Active Profiles</p>
            <h2 style="margin: 0.5rem 0; font-size: 2.2rem; font-weight: 700; color: #ffffff !important;">10</h2>
            <p style="margin: 0; font-size: 0.75rem; color: #a1a1aa;">• Role-based Access</p>
        </div>
        """,
        unsafe_allow_html=True
    )
with c4:
    import os
    is_offline = not os.environ.get("ANTHROPIC_API_KEY")
    status_color = "#fbbf24" if is_offline else "#34d399"
    status_label = "Mock Fallback (Offline)" if is_offline else "Connected"
    st.markdown(
        f"""
        <div class="glass-card" style="text-align: center; padding: 1.2rem; margin-bottom: 0;">
            <p style="margin: 0; font-size: 0.8rem; color: #ca8a04; font-weight: 600; text-transform: uppercase; letter-spacing: 0.05em;">AI Engine Status</p>
            <h2 style="margin: 0.5rem 0; font-size: 1.3rem; font-weight: 700; color: {status_color} !important; height: 3.3rem; display: flex; align-items: center; justify-content: center;">{status_label}</h2>
        </div>
        """,
        unsafe_allow_html=True
    )

st.write("")

# Highlighted Features Section
st.markdown("<h3 style='margin: 1.5rem 0 1rem 0; font-size: 1.5rem;'>🛠 Get Started with SkillForge</h3>", unsafe_allow_html=True)

col1, col2, col3 = st.columns(3, gap="large")

with col1:
    st.markdown(
        """
        <div class="glass-card" style="min-height: 250px;">
            <div style="font-size: 2rem; margin-bottom: 0.5rem;">📚</div>
            <h4>Explore the Skill Library</h4>
            <p>
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
            <h4>Create a Skill</h4>
            <p>
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
            <h4>Run Personas (GPTs)</h4>
            <p>
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
    <div class="glass-card" style="background: rgba(202, 138, 4, 0.03) !important; border-color: rgba(202, 138, 4, 0.25) !important;">
        <h4 style="margin: 0 0 0.5rem 0; color: #fef08a !important;">🔥 Feature Highlight: Wall Street AI Analyst Skill</h4>
        <p style="margin: 0; line-height: 1.6;">
            We have integrated a state-of-the-art <b>Financial Modelling Suite</b> including a database of <b>50 companies</b> and <b>10 premium tools</b>. 
            Test WACC calculations, DCF models, DuPont ROE decompositions, M&A history research, and generate investment reports instantly from the <b>Run</b> page by selecting the <b>Wall Street AI Analyst</b> persona.
        </p>
    </div>
    """,
    unsafe_allow_html=True
)
