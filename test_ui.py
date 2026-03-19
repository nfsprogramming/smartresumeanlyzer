
import streamlit as st
from app_utils.ui import setup_page_styling

print("Successfully imported utils.ui")
try:
    setup_page_styling()
    print("Successfully ran setup_page_styling (mock)")
except Exception as e:
    print(f"Error running setup_page_styling: {e}")
