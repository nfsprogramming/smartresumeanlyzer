"""
Mock Interview Page
"""

import streamlit as st
from modules.mock_interview import mock_interviewer
from utils.ui import setup_page_styling

st.set_page_config(page_title="Mock Interview", page_icon="🎤")
setup_page_styling()

st.title("🎤 AI Mock Interview")
st.markdown("### Practice your answers in real-time.")

# Initialize Chat History
if "messages" not in st.session_state:
    st.session_state.messages = []
    # Initial greeting
    st.session_state.messages.append({"role": "assistant", "content": "Hello! I'm your AI interviewer today. Ideally, we can start by you telling me a little about yourself?"})

# Display Chat
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

# User Input
if prompt := st.chat_input("Type your answer here..."):
    # Add user message
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)
        
    # Get AI Response
    with st.chat_message("assistant"):
        with st.spinner("Interviewer is listening..."):
            # Pass recent history
            response = mock_interviewer.get_response(st.session_state.messages[:-1], prompt)
            st.write(response)
            
    # Add AI message to history
    st.session_state.messages.append({"role": "assistant", "content": response})

# Sidebar controls
with st.sidebar:
    if st.button("Reset Interview"):
        st.session_state.messages = []
        st.rerun()
    st.info("Tip: Speak clearly and use the STAR method for behavioral questions.")
