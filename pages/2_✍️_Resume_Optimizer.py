"""
Resume Rewriter Page
"""

import streamlit as st
from modules.resume_rewriter import resume_rewriter
from utils.ui import setup_page_styling

st.set_page_config(page_title="Resume Optimizer", page_icon="✍️")
setup_page_styling()

st.title("✍️ AI Resume Optimizer")
st.markdown("### Tailor your resume for specific roles using Advanced AI.")

if 'resume_text' not in st.session_state or not st.session_state.resume_text:
    st.warning("⚠️ Please upload a resume on the Home page first.")
    st.stop()

# Input for target role
target_role = st.text_input("Target Job Role", placeholder="e.g. Senior Python Developer")

# Tab selection
tab1, tab2 = st.tabs(["Rewrite Section", "Generate Summary"])

with tab1:
    st.subheader("Rewrite Specific Section")
    input_text = st.text_area("Paste the section you want to rewrite (Experience, Summary, etc.)", height=200)
    
    if st.button("Rewrite with AI", type="primary"):
        if not input_text or not target_role:
            st.error("Please provide both text and a target role.")
        else:
            with st.spinner("AI is rewriting your text..."):
                rewritten = resume_rewriter.rewrite_section(input_text, target_role)
                st.success("✨ Rewritten Version:")
                st.info(rewritten)
                st.code(rewritten, language="text")

with tab2:
    st.subheader("Generate Professional Summary")
    jd_context = st.text_area("Paste Job Description (optional context)", height=150)
    
    if st.button("Generate Summary"):
        with st.spinner("Drafting perfect summary..."):
            summary = resume_rewriter.generate_tailored_summary(st.session_state.resume_text, jd_context)
            st.success("✨ AI Generated Summary:")
            st.write(summary)
            st.code(summary, language="text")
