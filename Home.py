"""
Smart Resume Analyzer 2.0
==========================
Enterprise-grade AI Resume Platform
"""

import streamlit as st
import pandas as pd
from config import Settings, APIKeys
from utils.text_processing import extract_text_from_file, clean_text, count_action_verbs
from utils.analysis_utils import extract_top_keywords, match_skills, semantic_similarity, generate_recommendations
from modules.skill_analyzer import skill_analyzer
from utils.ui import setup_page_styling, get_ai_animation, card
from streamlit_lottie import st_lottie

# Configure page
st.set_page_config(
    page_title=Settings.APP_NAME,
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Apply Premium UI
setup_page_styling()

# Application Header
c_logo, c_title = st.columns([1, 4])
with c_logo:
    lottie_ai = get_ai_animation()
    if lottie_ai:
        st_lottie(lottie_ai, height=120, key="logo_anim")
    else:
        st.image("https://img.icons8.com/color/96/000000/artificial-intelligence.png", width=100)
        
with c_title:
    st.title("Smart Resume AI")
    st.markdown("### The Enterprise-Grade Career Assistant")

# Sidebar
with st.sidebar:
    st.markdown("---")
    st.header("Navigation")
    st.info("👈 Select a tool from the menu to get started.")
    
    st.markdown("---")
    st.markdown("### Settings")
    model_mode = st.radio("AI Model", ["Fast (Local)", "Precise (GPT-4)"], index=0)
    
    st.markdown("---")
    st.caption(f"v{Settings.VERSION} | {Settings.AUTHOR}")

# Main Dashboard Landing
st.markdown("---")

col1, col2 = st.columns([2, 1])

with col1:
    st.markdown("""
    <div class="glass-container">
        <h3>👋 Welcome to Your AI Career Coach</h3>
        <p>This platform integrates advanced AI tools to help you land your dream job.</p>
        <ul>
            <li><strong>Resume Analysis</strong>: Deep ATS insights.</li>
            <li><strong>JD Fetcher</strong>: Auto-scrape job descriptions.</li>
            <li><strong>Skill Gap Analysis</strong>: Find what you are missing.</li>
            <li><strong>AI Rewrite</strong>: Tailor your content for any role.</li>
        </ul>
        <br>
        <p style="color: #FFD700; font-weight: bold;">Start by uploading your Master Resume below.</p>
    </div>
    """, unsafe_allow_html=True)
    
    uploaded_file = st.file_uploader("📂 Upload Resume (PDF/DOCX)", type=Settings.ALLOWED_RESUME_FORMATS)

with col2:
    st.markdown("""
    <div class="glass-container">
        <h4 style="color:#00BFFF">⚡ System Status</h4>
        <p>✅ AI Engine: <strong>Online</strong></p>
        <p>✅ Database: <strong>Connected</strong></p>
        <p>✅ NLP Core: <strong>Ready</strong></p>
    </div>
    """, unsafe_allow_html=True)
    
    if APIKeys.OPENAI_API_KEY:
        st.success("✅ OpenAI API Connected")
    else:
        st.warning("⚠️ OpenAI Key Missing")

# Session State for Resume
if 'resume_text' not in st.session_state:
    st.session_state.resume_text = ""
if 'resume_name' not in st.session_state:
    st.session_state.resume_name = ""

if uploaded_file:
    # Process only if new file
    if uploaded_file.name != st.session_state.resume_name:
        with st.spinner("Processing document..."):
            text = extract_text_from_file(uploaded_file)
            cleaned_text = clean_text(text)
            
            st.session_state.resume_text = cleaned_text
            st.session_state.resume_name = uploaded_file.name
            st.success("Resume loaded successfully!")

if st.session_state.resume_text:
    st.markdown("---")
    st.subheader(f"📊 Resume Overview: {st.session_state.resume_name}")
    
    # Quick Stats
    wc = len(st.session_state.resume_text.split())
    verbs = count_action_verbs(st.session_state.resume_text)
    found_skills, missing_skills = match_skills(st.session_state.resume_text)
    
    m1, m2, m3 = st.columns(3)
    with m1:
        st.metric("Word Count", wc, delta=None)
    with m2:
        st.metric("Action Verbs", verbs, help="Aim for 20+ strong verbs")
    with m3:
         st.metric("Found Skills", len(found_skills), "Great")
         
    # Proficiency Preview
    if found_skills:
        st.markdown("### 🧬 Skill DNA")
        prof_map = skill_analyzer.analyze_proficiency(st.session_state.resume_text, found_skills)
        
        # Simple Chips
        html = ""
        for skill in found_skills[:15]:
            level = prof_map.get(skill, "Beginner")
            color = "#FFD700" if level == "Advanced" else "#00BFFF" if level == "Intermediate" else "#A0A0A0"
            html += f"<span style='background-color: {color}22; border: 1px solid {color}; padding: 4px 10px; border-radius: 12px; margin-right: 5px; color: {color}; display: inline-block; margin-bottom: 5px;'>{skill} • {level[0]}</span>"
        st.markdown(html, unsafe_allow_html=True)
         
    st.markdown("""
    ### 🚀 Next Steps
    
    Navigate to the **Sidebar** to use specific tools:
    
    1. **JD Fetcher**: Find a job to apply to.
    2. **Resume Optimizer**: Tailor your resume.
    3. **Project Ideas**: Build your portfolio.
    """)
