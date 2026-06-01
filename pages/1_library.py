"""
Library page — browse, run, edit, and delete skills.
"""
import streamlit as st
from core.storage.database import get_session
from core.storage.crud import list_skills, delete_skill
from core.ui import render_sidebar

st.set_page_config(page_title="Library — SkillForge", page_icon="📚", layout="wide")

# Render custom premium sidebar
render_sidebar("library")

st.markdown("<h1 class='main-header'>📚 Skill Library</h1>", unsafe_allow_html=True)
st.markdown("<h3 style='margin-top: -1.2rem; color: #94a3b8 !important; font-weight: 400 !important; font-size: 1.1rem; margin-bottom: 2rem;'>Browse and deploy custom-built AI skills & personas across the organization.</h3>", unsafe_allow_html=True)

session = get_session()
try:
    # Include hidden=False to only show active skills
    skills = list_skills(session, include_hidden=False)
except Exception as e:
    st.error(f"Error fetching library: {e}")
    skills = []
finally:
    session.close()

if not skills:
    st.info("No skills yet — go to **Create** to build the first one.")
    st.stop()

# Render cards in a 2-column layout
cols = st.columns(2, gap="large")

for i, skill in enumerate(skills):
    col = cols[i % 2]
    
    # Construct initials for avatar
    words = skill.name.split()
    initials = "".join([w[0].upper() for w in words[:2]])
    
    # Generate badges
    badges_html = f"""
    <div style="display: flex; gap: 0.5rem; margin: 0.5rem 0 1rem 0;">
        <span class="custom-badge badge-primary">v{skill.version}</span>
        <span class="custom-badge badge-success">Author: {skill.author}</span>
        {"<span class='custom-badge badge-secondary'>MCP Powered</span>" if "tools:" in (skill.content or "") else ""}
    </div>
    """
    
    with col:
        # We wrap the card layout in our custom glassmorphic styling
        st.markdown(
            f"""
            <div class="glass-card" style="margin-bottom: 1.5rem;">
                <div style="display: flex; align-items: center; margin-bottom: 0.75rem;">
                    <div class="persona-avatar" style="width: 44px; height: 44px; font-size: 1.1rem; margin-right: 1rem;">
                        {initials}
                    </div>
                    <div>
                        <h4 style="margin: 0; font-size: 1.3rem; color: #ffffff !important;">{skill.name}</h4>
                        <p style="margin: 0; font-size: 0.8rem; color: #64748b;">Created by {skill.author}</p>
                    </div>
                </div>
                {badges_html}
                <p style="font-size: 0.9rem; color: #cbd5e1; line-height: 1.6; min-height: 50px;">
                    {skill.description}
                </p>
            </div>
            """,
            unsafe_allow_html=True
        )
        
        # Action buttons directly below the card
        c_run, c_edit, c_del = st.columns([2, 1, 1])
        
        with c_run:
            if st.button("▶ Run Skill", key=f"run_{skill.id}", use_container_width=True):
                st.session_state["run_skill_id"] = skill.id
                st.session_state["run_skill_name"] = skill.name
                st.session_state.pop("run_messages", None)
                st.switch_page("pages/3_run.py")
                
        with c_edit:
            if st.button("✏️ Edit", key=f"edit_{skill.id}", use_container_width=True, type="secondary" if hasattr(st, "button") else "primary"):
                # Clear any previous create/edit session state
                for key in ["create_messages", "create_llm_messages", "create_draft",
                            "create_saved_id", "create_pending_files", "create_testing"]:
                    st.session_state.pop(key, None)
                st.session_state["edit_skill_id"] = skill.id
                st.switch_page("pages/2_create.py")
                
        with c_del:
            if st.session_state.get(f"confirm_delete_{skill.id}"):
                if st.button("Sure?", key=f"confirm_{skill.id}", use_container_width=True, type="primary"):
                    db_session = get_session()
                    try:
                        delete_skill(db_session, skill.id)
                    finally:
                        db_session.close()
                    st.session_state.pop(f"confirm_delete_{skill.id}", None)
                    st.rerun()
            else:
                if st.button("🗑 Del", key=f"delete_{skill.id}", use_container_width=True, type="secondary" if hasattr(st, "button") else "primary"):
                    st.session_state[f"confirm_delete_{skill.id}"] = True
                    st.rerun()
        
        st.write("") # Spacer
