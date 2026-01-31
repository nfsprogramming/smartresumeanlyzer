"""
Learning Path Page
"""

import streamlit as st
from modules.course_aggregator import course_aggregator
from utils.analysis_utils import match_skills
from utils.ui import setup_page_styling

st.set_page_config(page_title="Learning Path", page_icon="📚")
setup_page_styling()

st.title("📚 Personalized Learning Path")
st.markdown("### Free resources to bridge your skill gaps.")

if 'resume_text' not in st.session_state or not st.session_state.resume_text:
    st.warning("⚠️ Please upload a resume on the Home page first.")
    st.stop()

# 1. Identify Skills to Learn
st.subheader("1. Your Skill Gaps")
found, missing = match_skills(st.session_state.resume_text)

# Let user manually add or remove
selected_skills = st.multiselect("Select skills to learn:", options=missing + found, default=missing[:3])

if st.button("Generate Roadmap", type="primary"):
    with st.spinner("Curating free courses..."):
        roadmap = course_aggregator.get_learning_path(selected_skills)
        
        st.subheader("2. Your Roadmap")
        
        for skill, resources in roadmap.items():
            st.markdown(f"#### 📘 {skill}")
            cols = st.columns(len(resources))
            for i, res in enumerate(resources):
                if not isinstance(res, dict):
                    continue
                    
                with cols[i]:
                    # Determine icon
                    icon = "📺" if res.get('type') == "Video" else "📄" if res.get('type') == "Article" else "🎓"
                    
                    st.markdown(f"""
                        <div class="glass-container" style="padding: 15px; height: 100%;">
                            <div style="font-size: 24px; margin-bottom: 10px;">{icon}</div>
                            <div style="font-weight: bold; color: #00BFFF; margin-bottom: 5px;">{res.get('platform', 'Web')}</div>
                            <div style="font-size: 14px; margin-bottom: 10px;">{res.get('title', 'Link')}</div>
                            <a href="{res.get('url', '#')}" target="_blank" style="
                                text-decoration: none; 
                                color: white; 
                                background: #2b5876; 
                                padding: 5px 10px; 
                                border-radius: 5px; 
                                font-size: 12px;
                            ">Start Learning</a>
                        </div>
                    """, unsafe_allow_html=True)
                    
                    # Optional Video Preview if YouTube
                    if "youtube.com" in res['url'] or "youtu.be" in res['url']:
                        st.video(res['url'])
            st.markdown("<br>", unsafe_allow_html=True)
