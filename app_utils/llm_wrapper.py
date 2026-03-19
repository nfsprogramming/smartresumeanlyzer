"""
LLM Wrapper Module
Centralizes AI calls. Uses OpenAI if available, otherwise defaults to Pollinations.ai (Free).
"""

import os
import requests
import json
from config import APIKeys, Settings

# Pollinations AI Endpoint (Free, No Auth)
POLLINATIONS_BASE_URL = "https://text.pollinations.ai/"

def generate_text(prompt: str, system_role: str = "You are a helpful career assistant.", model: str = "openai") -> str:
    """
    Generates text using the best available AI backend.
    Priority:
    1. OpenAI API (if Key is set) - 'Precise'
    2. Pollinations.ai (Free/Fast) - 'Fast'
    """
    
    # 1. Try OpenAI if Key exists
    if APIKeys.OPENAI_API_KEY and APIKeys.OPENAI_API_KEY.startswith("sk-"):
        try:
            from openai import OpenAI
            client = OpenAI(api_key=APIKeys.OPENAI_API_KEY)
            
            response = client.chat.completions.create(
                model="gpt-4o-mini", # Fast & Accurate
                messages=[
                    {"role": "system", "content": system_role},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7
            )
            return response.choices[0].message.content
        except Exception as e:
            print(f"OpenAI Error: {e}. Falling back to Pollinations.")
    
    # 2. Use Pollinations.ai (Free)
    # Pollinations text API is very simple: GET /prompt or POST
    # We will use the OpenAI-compatible endpoint logic or direct fetch.
    # Direct fetch is often faster for Pollinations.
    
    try:
        # Pollinations OpenAI-compatible endpoint
        headers = {'Content-Type': 'application/json'}
        payload = {
            "messages": [
                {"role": "system", "content": system_role},
                {"role": "user", "content": prompt}
            ],
            "model": "openai",
            "jsonMode": False
        }
        
        response = requests.post("https://text.pollinations.ai/", json=payload, timeout=10)
        
        if response.status_code == 200:
            return response.text
        else:
            print(f"Pollinations API Error: {response.status_code}")
            
    except Exception as e:
        print(f"Pollinations Connection Error: {e}")

    # Fallback to Mock/Offline Data logic moved out of except block to handle both network error and status error
    if Settings.ENABLE_MOCK_DATA:
        return _get_mock_response(prompt)
        
    return "AI Service Unavailable. Please check your internet or try again later."
    
def _get_mock_response(prompt: str) -> str:
    """Returns safe fallback responses when AI is down."""
    prompt_lower = prompt.lower()
    
    if "interview question" in prompt_lower or "model answer" in prompt_lower:
        return "Here is a model answer using the STAR method:\n\n**Situation:** In my previous role, we faced a similar challenge where legacy code was slowing down deployment.\n**Task:** I was tasked with optimizing the build pipeline.\n**Action:** I implemented caching and parallelized tests using Docker.\n**Result:** This reduced build time by 40%."
        
    if "json" in prompt_lower:
        return '["Tell me about yourself.", "What is your biggest weakness?", "Describe a difficult bug you fixed.", "How do you prioritize tasks?", "Why do you want to work here?"]'
        
    return "This is a simulated AI response. The external AI service is currently unavailable or busy. Please try again later or configure an OpenAI Key in settings."

class AIEngine:
    @staticmethod
    def chat(prompt, system="You are an expert career coach."):
        return generate_text(prompt, system)

ai_engine = AIEngine()
