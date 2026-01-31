"""
ATS Simulator Page
"""

import streamlit as st
from modules.ats_emulator import ats_emulator
from config import COMPANY_ATS_KEYWORDS
from utils.ui import setup_page_styling

st.set_page_config(page_title="ATS Simulator", page_icon="🏢")
setup_page_styling()

st.title("🏢 Enterprise ATS Simulator")
st.markdown("### Test your resume against specific company algorithms.")

if 'resume_text' not in st.session_state or not st.session_state.resume_text:
    st.warning("⚠️ Please upload a resume on the Home page first.")
else:
    companies = list(COMPANY_ATS_KEYWORDS.keys())
    selected_company = st.selectbox("Select Target Company", companies)
    
    if st.button(f"Simulate {selected_company} Scan", type="primary"):
        with st.spinner("Running proprietary algorithms..."):
            res = ats_emulator.simulate_scan(st.session_state.resume_text, selected_company)
            
            # Score
            score = res['score']
            color = "green" if score > 75 else "orange" if score > 50 else "red"
            
            c1, c2 = st.columns([1, 2])
            with c1:
                st.metric("Probability of Interview", f"{score}%")
                st.markdown(f"**Status:** :{color}[{res['status'].replace('_', ' ').upper()}]")
                if res['length_check'] != "Good":
                    st.warning(f"Length Alert: {res['length_check']}")
            
            with c2:
                st.subheader("🤖 System Feedback")
                for item in res['specific_feedback']:
                    if "✅" in item:
                        st.success(item)
                    else:
                        st.warning(item)
                        
                st.markdown("**Keyword Gaps:**")
                if res['missing_keywords']:
                    st.write(", ".join([f"`{k}`" for k in res['missing_keywords']]))
                else:
                    st.success("All target keywords found!")
