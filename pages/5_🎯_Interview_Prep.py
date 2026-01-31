"""
Interview Prep Page
"""

import streamlit as st
from modules.interview_prep import interview_coach
from utils.analysis_utils import match_skills
from utils.ui import setup_page_styling, get_lottie, colored_header
from streamlit_lottie import st_lottie

st.set_page_config(page_title="Interview Prep", page_icon="🎯", layout="wide")
setup_page_styling()

# Header with Animation
c1, c2 = st.columns([1, 4])
with c1:
    lottie = get_lottie("interview")
    if lottie:
        st_lottie(lottie, height=120)
    else:
        st.image("https://img.icons8.com/nolan/96/question-mark.png", width=80)
with c2:
    st.title("AI Interview Generator")
    st.markdown("### 🎯 Prepare with custom questions tailored to your profile.")

if 'resume_text' not in st.session_state or not st.session_state.resume_text:
    st.warning("⚠️ Please upload a resume on the Home page first.")
else:
    # Setup
    found, _ = match_skills(st.session_state.resume_text)
    
    st.markdown("---")
    
    colored_header("Configure Evaluation")
    
    col1, col2 = st.columns(2)
    with col1:
        role = st.text_input("Target Role", "Software Engineer")
    with col2:
        level = st.selectbox("Difficulty", ["Entry Level", "Intermediate", "Senior", "Expert"])
        
    if st.button("Generate Questions", type="primary"):
        with st.spinner("interviewer is thinking..."):
            questions = interview_coach.generate_questions(role, found[:5], level)
            st.session_state['interview_questions'] = questions
            
    # Display Questions
    if 'interview_questions' in st.session_state:
        st.markdown("### 📝 Your Interview Set")
        for i, q in enumerate(st.session_state['interview_questions']):
            with st.expander(f"Question {i+1}", expanded=True):
                st.markdown(f"#### {q}")
                
                if st.button(f"Show Model Answer", key=f"ans_{i}"):
                    with st.spinner("Generating answer..."):
                        answer = interview_coach.get_model_answer(q)
                        st.info(answer)
