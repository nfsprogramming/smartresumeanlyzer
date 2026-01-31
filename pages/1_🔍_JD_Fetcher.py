"""
JD Auto-Fetcher Page
"""

import streamlit as st
from modules.jd_fetcher import jd_fetcher
from utils.ui import setup_page_styling

st.set_page_config(page_title="JD Auto-Fetcher", page_icon="🔍")
setup_page_styling()

st.markdown("# 🔍 Job Description Auto-Fetcher")
st.markdown("### Extract JD effortlessly from LinkedIn, Indeed, and more.")

url = st.text_input("🔗 Paste Job Post URL:", placeholder="https://www.linkedin.com/jobs/view/...")

if st.button("Fetch Job Description", type="primary"):
    if not url:
        st.error("Please enter a URL.")
    else:
        with st.spinner("Fetching job details..."):
            jd_text = jd_fetcher.fetch_from_url(url)
            
            if jd_text:
                st.success("✅ Job Description Extracted!")
                st.text_area("Extracted Text", jd_text, height=400)
                
                # Option to save to session state to use in other pages
                if st.button("Use this JD for Analysis"):
                    st.session_state['jd_text'] = jd_text
                    st.success("JD saved to session! Go to Resume Analyzer.")
            else:
                st.error("Could not extract text. The site might be blocking scripts or the format is unsupported.")
