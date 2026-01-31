"""
Settings & Admin Page
"""

import streamlit as st
import os
from utils.ui import setup_page_styling

st.set_page_config(page_title="Settings", page_icon="⚙️")
setup_page_styling()

st.title("⚙️ System Settings")

# 1. API Configuration
st.subheader("🔑 API Keys")
st.info("These are loaded from your .env file. You can override them for this session here.")

openai_key = st.text_input("OpenAI API Key", type="password", placeholder="sk-...")
if openai_key:
    # In a real app, this should securely store it, but for Streamlit session:
    os.environ["OPENAI_API_KEY"] = openai_key
    st.success("Key updated for this session!")

# 2. Database Management
st.subheader("💾 Data Management")

c1, c2 = st.columns(2)
with c1:
    st.markdown("### Clear Session")
    st.markdown("Remove all uploaded resumes and temporary analysis data.")
    if st.button("🗑️ Clear Session State"):
        st.session_state.clear()
        st.success("Session cleared. Please refresh.")

with c2:
    st.markdown("### Reset Database")
    st.markdown("⚠️ **Danger Zone**: Delete all tracked jobs and metrics.")
    if st.button("🔥 Wipe Database", type="primary"):
        try:
            db_path = "database/resume_app.db" # Check config for exact path
            if os.path.exists(db_path):
                os.remove(db_path)
                st.success("Database deleted. Restart app to recreate schema.")
            else:
                st.warning("No database found.")
        except Exception as e:
            st.error(f"Error: {e}")

# 3. About
st.markdown("---")
st.markdown("### ℹ️ About")
st.write("Smart Resume Analyzer v2.0")
st.write("Built with Streamlit & Python")
