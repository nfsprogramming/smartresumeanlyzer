"""
Bias Check Page
"""

import streamlit as st
from modules.bias_detector import bias_detector
from app_utils.ui import setup_page_styling

st.set_page_config(page_title="Bias Detection", page_icon="🧠")
setup_page_styling()

st.title("🧠 Bias & Inclusivity Check")
st.markdown("### Ensure your resume appeals to a diverse range of recruiters.")

if 'resume_text' not in st.session_state or not st.session_state.resume_text:
    st.warning("⚠️ Please upload a resume on the Home page first.")
else:
    if st.button("Analyze Language", type="primary"):
        res = bias_detector.analyze_bias(st.session_state.resume_text)
        
        score = res["score"]
        st.metric("Inclusivity Score", f"{score}/100")
        
        if not res["findings"]:
             st.success("✅ Excellent! Your resume uses neutral, professional language.")
        else:
             st.subheader("Flags")
             for f in res["findings"]:
                 with st.expander(f"⚠️ {f['type']}", expanded=True):
                     st.write(f.get("msg"))
                     st.write(f"**Found:** `{', '.join(f['words'])}`")
                     
             st.info("💡 **Why this matters:** Unconscious bias exists in hiring. Neutralizing your language helps your skills stand out without triggering stereotypes.")
             
             if score < 80:
                 st.markdown("### Suggested Action")
                 st.write("Consider using the **Resume Rewriter** tool to rephrase these sections.")
