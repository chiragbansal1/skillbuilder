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
            /* Global typography */
            html, body, [class*="css"], .stApp {
                font-family: 'Inter', sans-serif;
                background-color: #0c0f16 !important;
                color: #e2e8f0;
            }
            
            h1, h2, h3, h4, h5, h6 {
                font-family: 'Outfit', sans-serif !important;
                font-weight: 600 !important;
                letter-spacing: -0.02em;
                color: #ffffff !important;
            }
            
            /* Main header gradient */
            .main-header {
                background: linear-gradient(135deg, #a5b4fc 0%, #6366f1 50%, #4338ca 100%);
                -webkit-background-clip: text;
                -webkit-text-fill-color: transparent;
                font-weight: 800;
                font-size: 3rem !important;
                margin-bottom: 0.5rem;
            }
            
            /* Sidebar styling */
            [data-testid="stSidebar"] {
                background-color: #07090e !important;
                border-right: 1px solid #1e293b !important;
                padding-top: 1rem;
            }
            
            /* Glassmorphic cards */
            .glass-card {
                background: rgba(30, 41, 59, 0.45);
                backdrop-filter: blur(12px);
                -webkit-backdrop-filter: blur(12px);
                border: 1px solid rgba(255, 255, 255, 0.08);
                border-radius: 16px;
                padding: 1.5rem;
                margin-bottom: 1.2rem;
                transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
            }
            
            .glass-card:hover {
                transform: translateY(-2px);
                border-color: rgba(99, 102, 241, 0.4);
                box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.3), 0 8px 10px -6px rgba(99, 102, 241, 0.1);
            }
            
            /* Badges */
            .custom-badge {
                display: inline-flex;
                align-items: center;
                border-radius: 9999px;
                padding: 0.25rem 0.75rem;
                font-size: 0.75rem;
                font-weight: 500;
                line-height: 1;
                margin-right: 0.5rem;
                margin-bottom: 0.5rem;
            }
            
            .badge-primary {
                background-color: rgba(99, 102, 241, 0.15);
                color: #a5b4fc;
                border: 1px solid rgba(99, 102, 241, 0.3);
            }
            
            .badge-success {
                background-color: rgba(16, 185, 129, 0.15);
                color: #34d399;
                border: 1px solid rgba(16, 185, 129, 0.3);
            }
            
            .badge-secondary {
                background-color: rgba(148, 163, 184, 0.15);
                color: #cbd5e1;
                border: 1px solid rgba(148, 163, 184, 0.3);
            }
            
            /* Premium buttons */
            .stButton>button {
                background: linear-gradient(135deg, #4f46e5 0%, #3730a3 100%) !important;
                color: #ffffff !important;
                border: none !important;
                border-radius: 8px !important;
                padding: 0.5rem 1.25rem !important;
                font-weight: 500 !important;
                transition: all 0.2s !important;
                box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06) !important;
            }
            
            .stButton>button:hover {
                transform: translateY(-1px) !important;
                box-shadow: 0 10px 15px -3px rgba(99, 102, 241, 0.3), 0 4px 6px -2px rgba(99, 102, 241, 0.1) !important;
                background: linear-gradient(135deg, #6366f1 0%, #4338ca 100%) !important;
            }
            
            .stButton>button:active {
                transform: translateY(1px) !important;
            }
            
            /* Custom secondary or delete buttons */
            .stButton>button[kind="secondary"] {
                background: rgba(30, 41, 59, 0.7) !important;
                color: #e2e8f0 !important;
                border: 1px solid rgba(255, 255, 255, 0.1) !important;
            }
            
            .stButton>button[kind="secondary"]:hover {
                background: rgba(51, 65, 85, 0.7) !important;
                border-color: rgba(255, 255, 255, 0.2) !important;
            }
            
            /* Persona item list in sidebar */
            .persona-item {
                display: flex;
                align-items: center;
                padding: 0.75rem 1rem;
                border-radius: 12px;
                margin-bottom: 0.5rem;
                cursor: pointer;
                border: 1px solid transparent;
                transition: all 0.2s ease;
                background-color: rgba(30, 41, 59, 0.2);
            }
            
            .persona-item:hover {
                background-color: rgba(99, 102, 241, 0.1);
                border-color: rgba(99, 102, 241, 0.2);
            }
            
            .persona-active {
                background-color: rgba(99, 102, 241, 0.15) !important;
                border-color: rgba(99, 102, 241, 0.4) !important;
                box-shadow: inset 0 0 12px rgba(99, 102, 241, 0.05);
            }
            
            .persona-avatar {
                width: 38px;
                height: 38px;
                border-radius: 50%;
                background: linear-gradient(135deg, #6366f1 0%, #a5b4fc 100%);
                color: white;
                display: flex;
                align-items: center;
                justify-content: center;
                font-family: 'Outfit', sans-serif;
                font-weight: 600;
                font-size: 0.9rem;
                margin-right: 0.75rem;
                box-shadow: 0 4px 10px rgba(99, 102, 241, 0.25);
                flex-shrink: 0;
            }
            
            .persona-details {
                flex-grow: 1;
                min-width: 0;
            }
            
            .persona-name {
                font-family: 'Outfit', sans-serif;
                font-size: 0.9rem;
                font-weight: 500;
                color: #ffffff;
                margin-bottom: 0.1rem;
                white-space: nowrap;
                overflow: hidden;
                text-overflow: ellipsis;
            }
            
            .persona-desc {
                font-size: 0.75rem;
                color: #94a3b8;
                white-space: nowrap;
                overflow: hidden;
                text-overflow: ellipsis;
            }
            
            /* Custom chat styling */
            .chat-container {
                display: flex;
                flex-direction: column;
                gap: 1.5rem;
                margin-bottom: 2rem;
            }
            
            .chat-bubble-user {
                background-color: #1e1b4b;
                border: 1px solid rgba(99, 102, 241, 0.2);
                border-radius: 16px 16px 4px 16px;
                padding: 1rem 1.25rem;
                align-self: flex-end;
                max-width: 80%;
                color: #f1f5f9;
                box-shadow: 0 4px 15px rgba(0, 0, 0, 0.2);
            }
            
            .chat-bubble-assistant {
                background-color: rgba(30, 41, 59, 0.6);
                border: 1px solid rgba(255, 255, 255, 0.05);
                border-radius: 16px 16px 16px 4px;
                padding: 1rem 1.25rem;
                align-self: flex-start;
                max-width: 85%;
                color: #f1f5f9;
                box-shadow: 0 4px 15px rgba(0, 0, 0, 0.15);
            }
            
            /* Code editor or markdown code display */
            code {
                font-family: 'Fira Code', monospace !important;
                font-size: 0.85rem !important;
                background-color: #0a0d14 !important;
                color: #e2e8f0 !important;
                padding: 0.15rem 0.35rem !important;
                border-radius: 4px !important;
            }
            
            pre {
                background-color: #07090e !important;
                border: 1px solid rgba(255, 255, 255, 0.05) !important;
                border-radius: 10px !important;
                padding: 1rem !important;
            }
            
            pre code {
                padding: 0 !important;
                background-color: transparent !important;
            }

            /* Customizing Streamlit's base elements */
            .stPageLink {
                background: transparent !important;
                border: none !important;
                transition: all 0.2s !important;
                padding: 0.5rem 0.75rem !important;
                border-radius: 8px !important;
            }
            
            .stPageLink:hover {
                background: rgba(255, 255, 255, 0.05) !important;
            }

            /* Offline badge */
            .offline-badge {
                background: rgba(245, 158, 11, 0.1);
                border: 1px solid rgba(245, 158, 11, 0.3);
                color: #fbbf24;
                padding: 0.35rem 0.75rem;
                border-radius: 8px;
                font-size: 0.8rem;
                font-weight: 500;
                display: flex;
                align-items: center;
                gap: 0.5rem;
                margin-bottom: 1.5rem;
            }
            .offline-dot {
                width: 8px;
                height: 8px;
                background-color: #f59e0b;
                border-radius: 50%;
                display: inline-block;
                box-shadow: 0 0 8px #f59e0b;
            }
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
