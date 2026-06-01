import streamlit as st
from core.storage.database import get_session
from core.storage.crud import list_skills

def inject_premium_css():
    """
    Inject premium glassmorphic and dark-cyber styling into the Streamlit app.
    """
    st.markdown(
        """
        <link rel="preconnect" href="https://fonts.googleapis.com">
        <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
        <link href="https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700&family=Inter:wght@300;400;500;600&family=Fira+Code:wght@400;500&display=swap" rel="stylesheet">
        <style>
            /* ═══ Global Theme: Champagne & Obsidian (Luxury Finance) ═══ */
            html, body, [class*="css"], .stApp {
                font-family: 'Inter', -apple-system, sans-serif;
                background: #000000 !important; /* Pure Obsidian Black */
                color: #cbd5e1;
                font-size: 16px !important;
            }
            
            /* Clean Streamlit Header */
            .stApp > header {
                background: transparent !important;
            }

            /* Make general markdown text highly readable and clean */
            div.stMarkdown p {
                font-size: 1.05rem !important;
                line-height: 1.65 !important;
                color: #cbd5e1 !important;
            }

            /* ═══ Typography ═══ */
            h1, h2, h3, h4, h5, h6 {
                font-family: 'Outfit', sans-serif !important;
                font-weight: 500 !important;
                letter-spacing: -0.01em;
                color: #ffffff !important;
            }
            .main-header {
                font-weight: 700 !important;
                font-size: 2.8rem !important; 
                margin-bottom: 0.8rem;
                /* Soft Champagne Gold text gradient */
                background: linear-gradient(135deg, #fef08a 0%, #ca8a04 100%);
                -webkit-background-clip: text;
                -webkit-text-fill-color: transparent;
                text-shadow: 0 2px 10px rgba(0,0,0,0.5); 
            }
            .main-subheader {
                margin-top: -1.2rem !important;
                color: #94a3b8 !important; 
                font-weight: 400 !important;
                font-size: 1.15rem !important;
                margin-bottom: 2.0rem !important;
                display: block;
            }

            /* ═══ Sidebar ═══ */
            [data-testid="stSidebar"] {
                background: #0f1016 !important;
                border-right: 1px solid rgba(202, 138, 4, 0.15) !important;
                padding-top: 1rem;
            }
            
            [data-testid="stSidebar"] .stMarkdown p, 
            [data-testid="stSidebar"] .stCheckbox label,
            [data-testid="stSidebar"] .stRadio label {
                font-size: 1.0rem !important;
                color: #94a3b8 !important;
            }

            [data-testid="stSidebar"] .stButton>button {
                background: rgba(255, 255, 255, 0.02) !important;
                border: 1px solid rgba(202, 138, 4, 0.2) !important;
                color: #fef08a !important;
                border-radius: 8px !important;
                font-size: 0.95rem !important;
                transition: all 0.2s ease !important;
            }
            [data-testid="stSidebar"] .stButton>button:hover {
                background: rgba(202, 138, 4, 0.1) !important;
                border-color: rgba(202, 138, 4, 0.4) !important;
            }

            /* ═══ Obsidian Cards with Champagne Gold borders ═══ */
            .glass-card {
                background: #09090b !important;
                border: 1px solid rgba(202, 138, 4, 0.15) !important; /* Gold border */
                border-radius: 12px !important;
                padding: 1.8rem !important;
                margin-bottom: 1.5rem !important;
                transition: all 0.25s cubic-bezier(0.4, 0, 0.2, 1) !important;
                box-shadow: inset 0 1px 0 rgba(255, 255, 255, 0.05), 
                            0 4px 12px rgba(0, 0, 0, 0.5) !important;
            }
            .glass-card:hover {
                transform: translateY(-2px) !important;
                background: #111115 !important;
                border-color: rgba(202, 138, 4, 0.4) !important; /* Brighter gold border */
                box-shadow: inset 0 1px 0 rgba(255, 255, 255, 0.1), 
                            0 12px 25px rgba(0, 0, 0, 0.6) !important;
            }
            .glass-card h4 {
                font-size: 1.4rem !important; 
            }
            .glass-card p {
                font-size: 1.0rem !important; 
                color: #94a3b8 !important;
            }

            /* ═══ Luxury Gold Buttons ═══ */
            .stButton>button {
                background: linear-gradient(135deg, #ca8a04 0%, #854d0e 100%) !important; /* Champagne/Amber gradient */
                color: #ffffff !important;
                border: none !important;
                border-radius: 8px !important;
                padding: 0.7rem 1.5rem !important;
                font-weight: 600 !important;
                font-size: 1.0rem !important; 
                transition: all 0.2s ease !important;
                box-shadow: inset 0 1px 0 rgba(255, 255, 255, 0.2), 
                            0 4px 12px rgba(202, 138, 4, 0.3) !important;
            }
            .stButton>button:hover {
                background: linear-gradient(135deg, #eab308 0%, #a16207 100%) !important;
                transform: translateY(-1px) !important;
                box-shadow: inset 0 1px 0 rgba(255, 255, 255, 0.3), 
                            0 6px 15px rgba(202, 138, 4, 0.4) !important;
            }
            .stButton>button[kind="secondary"] {
                background: rgba(255, 255, 255, 0.05) !important;
                color: #fef08a !important;
                border: 1px solid rgba(202, 138, 4, 0.3) !important;
                box-shadow: inset 0 1px 0 rgba(255, 255, 255, 0.05) !important;
            }
            .stButton>button[kind="secondary"]:hover {
                background: rgba(202, 138, 4, 0.1) !important;
                border-color: rgba(202, 138, 4, 0.5) !important;
            }

            /* ═══ Badges (Claude-style Tool Log Indicators) ═══ */
            .custom-badge {
                display: inline-flex;
                align-items: center;
                border-radius: 4px;
                padding: 0.15rem 0.4rem;
                font-size: 0.72rem !important; 
                font-family: 'ui-monospace', 'SFMono-Regular', monospace !important;
                font-weight: 400;
                margin-right: 0.4rem;
                margin-bottom: 0.4rem;
                letter-spacing: -0.01em;
            }
            .badge-primary {
                background: rgba(202, 138, 4, 0.12) !important;
                color: #fef08a !important;
                border: 1px solid rgba(202, 138, 4, 0.25) !important;
            }
            .badge-success {
                background: rgba(16, 185, 129, 0.12) !important;
                color: #6ee7b7 !important;
                border: 1px solid rgba(16, 185, 129, 0.25) !important;
            }
            .badge-secondary {
                background: rgba(255, 255, 255, 0.04) !important;
                color: #cbd5e1 !important;
                border: 1px solid rgba(255, 255, 255, 0.1) !important;
            }

            /* ═══ Persona Sidebar Items ═══ */
            .persona-item {
                display: flex;
                align-items: center;
                padding: 0.8rem 0.9rem; 
                border-radius: 8px;
                margin-bottom: 0.5rem;
                cursor: pointer;
                border: 1px solid transparent;
                background-color: transparent;
                transition: all 0.2s ease;
            }
            .persona-item:hover {
                background-color: rgba(255, 255, 255, 0.05);
            }
            .persona-active {
                background-color: rgba(202, 138, 4, 0.15) !important;
                border-color: rgba(202, 138, 4, 0.3) !important;
            }
            .persona-avatar {
                width: 38px; 
                height: 38px;
                border-radius: 8px;
                background: linear-gradient(135deg, #eab308, #854d0e);
                color: white;
                display: flex;
                align-items: center;
                justify-content: center;
                font-family: 'Outfit', sans-serif;
                font-weight: 600;
                font-size: 1.0rem;
                margin-right: 0.9rem;
                flex-shrink: 0;
                box-shadow: inset 0 1px 0 rgba(255,255,255,0.2), 0 2px 5px rgba(0,0,0,0.3);
            }
            .persona-name {
                font-family: 'Inter', sans-serif;
                font-size: 1.0rem; 
                font-weight: 600;
                color: #ffffff;
                margin-bottom: 0.15rem;
            }
            .persona-desc {
                font-size: 0.85rem; 
                color: #94a3b8;
            }

            /* ═══ Code & Chat ═══ */
            code {
                font-family: 'ui-monospace', 'SFMono-Regular', monospace !important;
                font-size: 0.9rem !important; 
                background: rgba(255, 255, 255, 0.05) !important;
                color: #fef08a !important;
                padding: 0.2rem 0.4rem !important;
                border-radius: 4px !important;
                border: 1px solid rgba(255, 255, 255, 0.1) !important;
            }
            pre {
                background: rgba(0, 0, 0, 0.3) !important;
                border: 1px solid rgba(255, 255, 255, 0.1) !important;
                border-radius: 10px !important;
                padding: 1.2rem !important;
                box-shadow: inset 0 2px 10px rgba(0,0,0,0.2);
            }
            /* ═══ Native Streamlit Chat Message Styling ═══ */
            [data-testid="stChatMessage"] {
                background-color: rgba(255, 255, 255, 0.03) !important;
                border: 1px solid rgba(255, 255, 255, 0.08) !important;
                border-radius: 12px !important;
                padding: 1.0rem 1.2rem !important;
                margin-bottom: 0.8rem !important;
                color: #e2e8f0 !important;
                box-shadow: 0 4px 12px rgba(0, 0, 0, 0.4) !important;
            }
            /* User Chat Message - Champagne gold border/tint */
            [data-testid="stChatMessage"]:has(img[alt="user"]),
            [data-testid="stChatMessage"]:has([data-testid="stChatMessageAvatarUser"]) {
                background-color: rgba(202, 138, 4, 0.06) !important;
                border-color: rgba(202, 138, 4, 0.25) !important;
            }
            [data-testid="stChatMessage"] p {
                font-size: 1.0rem !important;
                line-height: 1.55 !important;
                color: #e2e8f0 !important;
            }
            
            /* Inputs */
            .stTextInput input, .stTextArea textarea, .stSelectbox select {
                background: rgba(0, 0, 0, 0.25) !important;
                border: 1px solid rgba(202, 138, 4, 0.2) !important;
                border-radius: 8px !important;
                color: #f8fafc !important;
                font-size: 1.05rem !important;
                padding: 0.75rem 1rem !important;
                box-shadow: inset 0 2px 5px rgba(0,0,0,0.2);
            }
            .stTextInput input:focus, .stTextArea textarea:focus {
                border-color: #ca8a04 !important;
                background: rgba(0, 0, 0, 0.4) !important;
                box-shadow: inset 0 2px 5px rgba(0,0,0,0.3), 0 0 0 2px rgba(202,138,4,0.2) !important;
            }
            
            /* ═══ Status Badges ═══ */
            .offline-badge, .live-badge {
                padding: 0.4rem 0.8rem;
                border-radius: 6px;
                font-size: 0.8rem;
                font-weight: 500;
                display: flex;
                align-items: center;
                gap: 0.4rem;
                margin-bottom: 1rem;
            }
            .offline-badge {
                background: rgba(245, 158, 11, 0.1);
                border: 1px solid rgba(245, 158, 11, 0.2);
                color: #fbbf24;
            }
            .live-badge {
                background: rgba(16, 185, 129, 0.1);
                border: 1px solid rgba(16, 185, 129, 0.2);
                color: #34d399;
            }
            .offline-dot { width: 8px; height: 8px; background: #f59e0b; border-radius: 50%; }
            .live-dot { width: 8px; height: 8px; background: #10b981; border-radius: 50%; box-shadow: 0 0 5px rgba(16, 185, 129, 0.5); }
        </style>
        """,
        unsafe_allow_html=True
    )

def render_sidebar(active_page: str):
    """
    Render the custom SkillForge sidebar navigation, including the Custom GPT
    Personas list when on the run page, and user/offline state configurations.
    """
    inject_premium_css()
    
    import os
    from dotenv import load_dotenv
    load_dotenv()
    
    # Initialize session state for LLM config if not present
    if "llm_provider" not in st.session_state:
        # Load from config.yaml as default
        import yaml
        from pathlib import Path
        try:
            cfg = yaml.safe_load(Path("config.yaml").read_text())["llm"]
            st.session_state["llm_provider"] = cfg.get("provider", "gemini")
        except Exception:
            st.session_state["llm_provider"] = "gemini"
            
    if "gemini_api_key" not in st.session_state:
        st.session_state["gemini_api_key"] = os.environ.get("GEMINI_API_KEY", "")
    if "anthropic_api_key" not in st.session_state:
        st.session_state["anthropic_api_key"] = os.environ.get("ANTHROPIC_API_KEY", "")
        
    with st.sidebar:
        # App logo/branding
        st.markdown(
            """
            <div style="display: flex; align-items: center; margin-bottom: 1.5rem; margin-top: -1rem;">
                <div style="font-size: 2.2rem; margin-right: 0.5rem; filter: drop-shadow(0 0 8px rgba(99,102,241,0.6));">⚡</div>
                <div style="font-family: 'Outfit', sans-serif; font-size: 1.6rem; font-weight: 700; color: white;">SkillForge</div>
            </div>
            """, 
            unsafe_allow_html=True
        )
        
        # LLM Engine Configurator
        st.markdown("<p style='font-size: 0.75rem; font-weight: 600; color: #64748b; text-transform: uppercase; margin-bottom: 0.5rem; letter-spacing: 0.05em;'>🤖 LLM Engine Settings</p>", unsafe_allow_html=True)
        
        provider_options = ["Gemini (Google)", "Anthropic (Claude)", "Mock Offline Mode"]
        current_prov = st.session_state["llm_provider"]
        if current_prov == "gemini":
            provider_idx = 0
        elif current_prov == "claude":
            provider_idx = 1
        else:
            provider_idx = 2
            
        selected_provider_label = st.selectbox(
            "Provider",
            provider_options,
            index=provider_idx,
            key="llm_provider_selectbox",
            label_visibility="collapsed"
        )
        
        # Update provider in session state
        if selected_provider_label == "Gemini (Google)":
            st.session_state["llm_provider"] = "gemini"
        elif selected_provider_label == "Anthropic (Claude)":
            st.session_state["llm_provider"] = "claude"
        else:
            st.session_state["llm_provider"] = "mock"
            
        provider = st.session_state["llm_provider"]
        
        # Key inputs and status badge
        has_key = False
        if provider == "gemini":
            new_key = st.text_input(
                "Gemini API Key",
                value=st.session_state["gemini_api_key"],
                type="password",
                placeholder="AIzaSy...",
                help="Enter your Google Gemini API Key"
            )
            if new_key != st.session_state["gemini_api_key"]:
                st.session_state["gemini_api_key"] = new_key
                st.rerun()
            has_key = bool(st.session_state["gemini_api_key"])
            
        elif provider == "claude":
            new_key = st.text_input(
                "Anthropic API Key",
                value=st.session_state["anthropic_api_key"],
                type="password",
                placeholder="sk-ant-...",
                help="Enter your Anthropic Claude API Key"
            )
            if new_key != st.session_state["anthropic_api_key"]:
                st.session_state["anthropic_api_key"] = new_key
                st.rerun()
            has_key = bool(st.session_state["anthropic_api_key"])
            
        # Display Connection Status Badge
        if provider == "mock":
            st.markdown(
                """
                <div class="offline-badge" style="margin-top: 0.5rem; margin-bottom: 1rem;">
                    <span class="offline-dot"></span>
                    <span>Mock Mode Active (Offline)</span>
                </div>
                """,
                unsafe_allow_html=True
            )
        elif has_key:
            st.markdown(
                """
                <div style="background: rgba(16, 185, 129, 0.1); border: 1px solid rgba(16, 185, 129, 0.3); color: #34d399; padding: 0.35rem 0.75rem; border-radius: 8px; font-size: 0.8rem; font-weight: 500; display: flex; align-items: center; gap: 0.5rem; margin-top: 0.5rem; margin-bottom: 1rem;">
                    <span style="width: 8px; height: 8px; background-color: #10b981; border-radius: 50%; display: inline-block; box-shadow: 0 0 8px #10b981;"></span>
                    <span>LLM connected (Live key)</span>
                </div>
                """,
                unsafe_allow_html=True
            )
        else:
            st.markdown(
                """
                <div class="offline-badge" style="margin-top: 0.5rem; margin-bottom: 1rem;">
                    <span class="offline-dot"></span>
                    <span>Mock Fallback (Key missing)</span>
                </div>
                """,
                unsafe_allow_html=True
            )
            
        # Custom navigation link list
        st.markdown("<p style='font-size: 0.75rem; font-weight: 600; color: #64748b; text-transform: uppercase; margin-bottom: 0.5rem; letter-spacing: 0.05em;'>Navigation</p>", unsafe_allow_html=True)
        
        st.page_link("app.py", label="Home", icon="🏠")
        st.page_link("pages/1_library.py", label="Library", icon="📚")
        st.page_link("pages/2_create.py", label="Create", icon="✨")
        st.page_link("pages/3_run.py", label="Run Skill / Chat", icon="💬")
        
        st.divider()
        
        # Fetch skills for the Persona/GPT sidebar
        session = get_session()
        try:
            skills = list_skills(session, include_hidden=False)
        except Exception:
            skills = []
        finally:
            session.close()
            
        # Render the custom GPT Personas section
        st.markdown("<p style='font-size: 0.75rem; font-weight: 600; color: #64748b; text-transform: uppercase; margin-bottom: 0.5rem; letter-spacing: 0.05em;'>AI Personas (GPTs)</p>", unsafe_allow_html=True)
        
        if not skills:
            st.caption("No skills available. Go to Create to build one.")
        else:
            active_skill_id = st.session_state.get("run_skill_id")
            
            # Create a scrolling panel for personas
            for skill in skills:
                # Build initials for avatar
                words = skill.name.split()
                initials = "".join([w[0].upper() for w in words[:2]])
                
                # Active styling class
                is_active = (active_skill_id == skill.id and active_page == "run")
                active_class = "persona-active" if is_active else ""
                
                # Render the clickable button styled like a custom GPT
                # Since Streamlit buttons submit a rerun, we use a standard key
                # We render HTML container but need a button trigger inside or use streamlit buttons styled nicely
                # For pure streamliness: we can use streamlit buttons that look like GPT cards, or a select box or styled buttons.
                # Let's use st.button but styled using our class, using html injection for display and standard st.button inside columns for triggers
                # Wait, st.button with key is the most robust way to trigger in Streamlit.
                # Let's render the visual card, and right inside/over it a streamlit button
                # Or even simpler: we can use a standard Streamlit button with a custom label like f"🤖 {skill.name}"
                # Let's make it look extremely custom using markdown + button.
                # We can do:
                btn_label = f"🤖 {skill.name}"
                if is_active:
                    btn_label = f"🔥 {skill.name} (Active)"
                
                if st.button(
                    btn_label, 
                    key=f"sidebar_gpt_{skill.id}", 
                    use_container_width=True,
                    help=skill.description
                ):
                    st.session_state["run_skill_id"] = skill.id
                    st.session_state["run_skill_name"] = skill.name
                    st.session_state.pop("run_messages", None)
                    if active_page != "run":
                        st.switch_page("pages/3_run.py")
                    else:
                        st.rerun()
                        
        st.divider()
        
        # User selection section
        st.markdown("<p style='font-size: 0.75rem; font-weight: 600; color: #64748b; text-transform: uppercase; margin-bottom: 0.25rem; letter-spacing: 0.05em;'>Profile</p>", unsafe_allow_html=True)
        from shared import FAKE_USERS
        st.session_state.setdefault("current_user", FAKE_USERS[0])
        current_idx = FAKE_USERS.index(st.session_state["current_user"]) if st.session_state["current_user"] in FAKE_USERS else 0
        new_user = st.selectbox(
            "Signed in as",
            FAKE_USERS,
            index=current_idx,
            label_visibility="collapsed"
        )
        if new_user != st.session_state["current_user"]:
            st.session_state["current_user"] = new_user
            st.rerun()
            
        # Clear chat helper
        if active_page == "run":
            if st.button("🗑 Clear Active Chat", use_container_width=True, type="secondary" if hasattr(st, "button") else "primary"):
                st.session_state.pop("run_messages", None)
                st.rerun()
