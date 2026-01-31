"""
Resume Intelligence Page
"""

import streamlit as st
import plotly.express as px
import matplotlib.pyplot as plt
from wordcloud import WordCloud
from modules.authenticity_checker import authenticity_checker
from modules.soft_skill_analyzer import soft_skill_analyzer
from modules.heatmap_generator import heatmap_generator
from utils.ui import setup_page_styling, get_lottie
from streamlit_lottie import st_lottie

st.set_page_config(page_title="Resume Intelligence", page_icon="🧠", layout="wide")
setup_page_styling()

c1, c2 = st.columns([1, 4])
with c1:
    lottie = get_lottie("ai")
    if lottie:
        st_lottie(lottie, height=100)
    else:
        st.markdown("🧠")
with c2:
    st.title("Resume Intelligence Suite")
    st.markdown("### Advanced analytics: Authenticity, Soft Skills, and Structure.")

if 'resume_text' not in st.session_state or not st.session_state.resume_text:
    st.warning("⚠️ Please upload a resume on the Home page first.")
else:
    resume_text = st.session_state.resume_text
    
    t1, t2, t3 = st.tabs(["⚠️ Authenticity Check", "🧠 Soft Skills", "🔥 Heatmap & Structure"])
    
    # --- Tab 1: Authenticity ---
    with t1:
        st.subheader("Authenticity & Red Flag Detector")
        auth_res = authenticity_checker.analyze_claims(resume_text)
        
        # Dial Chart
        score = auth_res["score"]
        color = "green" if score > 80 else "orange" if score > 50 else "red"
        
        c1, c2 = st.columns([1, 2])
        with c1:
            st.metric("Trust Score", f"{score}/100", delta="-Risk" if score < 100 else "Perfect")
            st.caption(f"Verdict: **{auth_res['verdict']}**")
            
        with c2:
            if auth_res["flags"]:
                st.error("🚩 Potential Issues Detected:")
                for flag in auth_res["flags"]:
                    st.write(f"- {flag}")
            else:
                st.success("✅ No obvious red flags detected.")
                
        st.info("ℹ️ note: This is an automated heuristic check. Always verify with human review.")

    # --- Tab 2: Soft Skills ---
    with t2:
        st.subheader("Soft Skill & Tone Analysis")
        soft_res = soft_skill_analyzer.analyze(resume_text)
        
        # Tone
        tone = soft_res.pop("ToneAnalysis")
        k1, k2 = st.columns(2)
        with k1:
             st.markdown(f"**Tone:** {tone['Sentiment']}")
        with k2:
             st.markdown(f"**Writing Style:** {tone['Style']}")
        
        st.divider()
        
        # Radar Chart for Soft Skills
        categories = list(soft_res.keys())
        scores = [soft_res[k]["score"] for k in categories]
        
        # Using Plotly
        df_radar = dict(
            r=scores,
            theta=categories
        )
        fig = px.line_polar(df_radar, r='r', theta='theta', line_close=True)
        fig.update_traces(fill='toself')
        fig.update_layout(polar=dict(radialaxis=dict(visible=True, range=[0, 100])))
        
        c_radar, c_detail = st.columns([1, 1])
        with c_radar:
            st.plotly_chart(fig, use_container_width=True)
            
        with c_detail:
            for cat in categories:
                data = soft_res[cat]
                with st.expander(f"{cat} ({data['level']})"):
                    st.progress(data['score'])
                    if data['evidence']:
                        st.write(f"Evidence: {', '.join(data['evidence'])}")
                    else:
                        st.caption("No explicit keywords found.")

    # --- Tab 3: Heatmap ---
    with t3:
        st.subheader("Structure & Content Heatmap")
        
        # 1. Section Analysis Table
        df = heatmap_generator.generate_section_analysis(resume_text)
        
        # Visualize Strength
        fig_bar = px.bar(df, x='Section', y='Strength Score', color='Strength Score', 
                         color_continuous_scale='Viridis', title="Section Strength Analysis")
        st.plotly_chart(fig_bar, use_container_width=True)
        
        st.markdown("### Detailed Breakdown")
        st.dataframe(df, use_container_width=True)
        
        st.divider()
        st.markdown("### ☁️ Keyword Cloud")
        
        # Word Cloud
        try:
            wc = WordCloud(width=800, height=400, background_color='black', colormap='cool').generate(resume_text)
            fig_wc, ax = plt.subplots()
            ax.imshow(wc, interpolation='bilinear')
            ax.axis("off")
            st.pyplot(fig_wc)
        except Exception as e:
            st.error(f"Could not generate word cloud: {e}")
