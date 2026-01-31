"""
Student Coach Page
"""

import streamlit as st
from modules.student_mode import student_coach
from utils.ui import setup_page_styling

st.set_page_config(page_title="Student Mode", page_icon="🎓")
setup_page_styling()

st.title("🎓 Student Career Coach")
st.markdown("### Optimized analysis for Freshers & Interns.")

if 'resume_text' not in st.session_state or not st.session_state.resume_text:
    st.warning("⚠️ Please upload a resume on the Home page first.")
else:
    st.info("ℹ️ switching to **Fresher Mode**: Prioritizing Projects, Campus Impact, and Learning Potential over Work Experience.")
    
    if st.button("Run Student Audit", type="primary"):
        res = student_coach.analyze_fresher_potential(st.session_state.resume_text)
        
        # Dial
        score = res["score"]
        c1, c2 = st.columns([1, 2])
        with c1:
            st.metric("Fresher Potential", f"{score}/100")
            st.caption(f"Verdict: **{res['verdict']}**")
            
        with c2:
            st.subheader("📝 Feedback")
            for item in res["feedback"]:
                if "✅" in item:
                    st.success(item)
                elif "⚠️" in item:
                    st.warning(item)
                else:
                    st.info(item)
                    
        st.divider()
        st.subheader("💡 Tips for Students")
        st.markdown("""
        - **Projects > Experience**: If key experience is missing, treat your top 3 class projects as "Experience".
        - **Hackathons**: List every hackathon participation, even if you didn't win. It shows passion.
        - **Relevant Coursework**: List 4-6 specific courses relevant to the job (e.g., "Data Structures", "OS").
        - **GitHub**: Make sure your profile is green! (Use our GitHub tool).
        """)
