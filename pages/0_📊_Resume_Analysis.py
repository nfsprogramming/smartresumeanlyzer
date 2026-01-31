"""
Resume Analysis Page
Legacy detailed analysis view
"""

import streamlit as st
import pandas as pd
import re
from config import Settings
from utils.text_processing import count_action_verbs, clean_text
from utils.analysis_utils import extract_top_keywords, match_skills, semantic_similarity, generate_recommendations
from modules.skill_analyzer import skill_analyzer
from utils.ui import setup_page_styling

st.set_page_config(page_title="Deep Resume Analysis", page_icon="📊", layout="wide")
setup_page_styling()

st.markdown("# 📊 Deep Resume Analysis")

# Check session state
if 'resume_text' not in st.session_state or not st.session_state.resume_text:
    st.warning("⚠️ Please upload a resume on the Home page first.")
    st.info("Tip: Go to the main app page to upload your resume.")
    st.stop()
    
resume_text = st.session_state.resume_text

# JD Input for Comparison
st.subheader("Compare with Job Description")
jd_input = st.text_area("Paste Job Description for comparison:", height=150)

# Check if JD was fetched from JD Fetcher tool
if 'jd_text' in st.session_state and st.session_state.jd_text:
    if st.button("Use Fetched JD"):
        jd_input = st.session_state.jd_text

if st.button("Run Full Analysis", type="primary"):
    with st.spinner("Crunching numbers..."):
        
        # 1. Metrics
        found_skills, missing_skills = match_skills(resume_text)
        
        # 2. JD Analysis (if present)
        sim_percent = 0.0
        top_keywords = []
        kw_rows = []
        recs = []
        
        if jd_input:
            sim = semantic_similarity(resume_text, jd_input)
            sim_percent = round(sim * 100, 1)
            top_keywords = extract_top_keywords(jd_input, top_k=15)
            
            # Check keywords
            for kw in top_keywords:
                present = bool(re.search(r"\b" + re.escape(kw) + r"\b", resume_text, flags=re.I))
                kw_rows.append({"Keyword": kw, "Found": "✅" if present else "❌"})
                
            recs = generate_recommendations(resume_text, jd_input, top_keywords, found_skills, missing_skills, sim)
        else:
            recs = ["Add a Job Description to get targeted recommendations."]

        # 3. Metrics
        col1, col2, col3 = st.columns(3)
        with col1:
             st.metric("Skill Count", len(found_skills))
        with col2:
             st.metric("ATS Match Score", f"{sim_percent}%" if jd_input else "N/A")
        with col3:
             st.metric("Action Verbs", count_action_verbs(resume_text))

        # --- Visual Analytics ---
        v1, v2 = st.columns([2, 1])
        with v1:
            st.markdown("#### 🕸️ Skill DNA (Proficiency)")
            if found_skills:
                # Prepare data for Radar Chart
                prof_map = skill_analyzer.analyze_proficiency(resume_text, found_skills)
                values = []
                skills_to_show = list(found_skills)[:8] # Limit to top 8
                for s in skills_to_show:
                    lvl = prof_map.get(s, "Beginner")
                    values.append(100 if lvl == "Advanced" else 66 if lvl == "Intermediate" else 33)
                
                import plotly.graph_objects as go
                fig = go.Figure(data=go.Scatterpolar(
                    r=values, theta=skills_to_show, fill='toself',
                    line_color='#00BFFF', fillcolor='rgba(0, 191, 255, 0.3)'
                ))
                fig.update_layout(
                    polar=dict(radialaxis=dict(visible=True, range=[0, 100]), angularaxis=dict(color="#fff")),
                    showlegend=False, paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
                    height=350, margin=dict(l=40, r=40, t=10, b=10)
                )
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.info("Upload a resume to see your Skill DNA.")

        with v2:
            st.markdown("#### ☁️ Keyword Cloud")
            try:
                from wordcloud import WordCloud
                import matplotlib.pyplot as plt
                
                clean_resume = clean_text(resume_text)
                wordcloud = WordCloud(
                    width=400, height=400, background_color=None, mode="RGBA",
                    colormap="Blues", max_words=50
                ).generate(clean_resume)
                
                fig, ax = plt.subplots(figsize=(5, 5))
                ax.imshow(wordcloud, interpolation='bilinear')
                ax.axis("off")
                fig.patch.set_facecolor('none')
                st.pyplot(fig)
            except Exception as e:
                st.info("Keyword cloud preview unavailable.")

        # 4. Tabs
        t1, t2, t3, t4 = st.tabs(["💡 Recommendations", "🛠 Skills & Proficiency", "📊 Keywords", "📝 Text"])
        
        with t1:
            for r in recs:
                st.info(r)
                
        with t2:
            c1, c2 = st.columns(2)
            with c1:
                st.markdown("### ✅ Detected Skills")
                if found_skills:
                    prof_map = skill_analyzer.analyze_proficiency(resume_text, found_skills)
                    for skill in found_skills:
                        level = prof_map.get(skill, "Beginner")
                        color = "#FFD700" if level == "Advanced" else "#455EB5" if level == "Intermediate" else "#CCCCCC"
                        st.markdown(f"**{skill}** — <span style='color:{color}'>{level}</span>", unsafe_allow_html=True)
                else:
                    st.write("No skills found.")
            with c2:
                st.markdown("### ⚠️ Missing / Suggested")
                if missing_skills: 
                    st.write(", ".join(missing_skills[:20]))
        
        with t3:
            if kw_rows:
                st.dataframe(pd.DataFrame(kw_rows), use_container_width=True)
            else:
                st.info("Enter a JD to see keyword analysis.")
                
        with t4:
            st.text_area("Parsed Text", resume_text, height=300)
