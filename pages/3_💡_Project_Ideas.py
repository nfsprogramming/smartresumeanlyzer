"""
Project Recommendations Page
"""

import streamlit as st
import pandas as pd
from modules.skill_analyzer import skill_analyzer
from modules.project_recommender import project_recommender
from utils.analysis_utils import match_skills
from utils.ui import setup_page_styling

st.set_page_config(page_title="Project Ideas", page_icon="💡")
setup_page_styling()

st.title("💡 Smart Project Recommendations")
st.markdown("### Boost your portfolio with projects that fill your skill gaps.")

if 'resume_text' not in st.session_state or not st.session_state.resume_text:
    st.warning("⚠️ Please upload a resume on the Home page first.")
else:
    # 1. Analyze Skills
    st.subheader("1. Skill Gap Analysis")
    found_skills, missing_skills = match_skills(st.session_state.resume_text)
    
    st.write(f"**Detected Skills:** {', '.join(found_skills[:10])}...")
    
    # Allow user to add target skills they WANT to learn/highlight
    target_skills_input = st.text_input("Add specific skills you want to target (comma separated):")
    if target_skills_input:
        extras = [s.strip() for s in target_skills_input.split(',')]
        missing_skills.extend(extras)

    # 2. Recommend Projects
    st.subheader("2. Recommended Repositories & Projects")
    
    if st.button("Generate Ideas", type="primary"):
        with st.spinner("Analyzing skill gaps and finding projects..."):
            # Use top missing skills + user input
            target_gaps = missing_skills[:5] if missing_skills else ["Python", "React"] # Fallbacks
            
            recommendations = project_recommender.get_recommendations(target_gaps)
            
            if recommendations:
                for proj in recommendations:
                    with st.expander(f"🚀 {proj['name']} ({proj['difficulty']})", expanded=True):
                        st.markdown(f"**Description:** {proj['description']}")
                        st.markdown(f"**Tech Stack:** `{', '.join(proj['skills'])}`")
                        if 'reason' in proj:
                            st.info(f"💡 Why: {proj['reason']}")
            else:
                st.info("No specific matches found. Try adding more target skills.")

    st.markdown("---")
    st.info("💡 **Pro Tip:** Host these projects on GitHub with a clean README to impress recruiters.")
