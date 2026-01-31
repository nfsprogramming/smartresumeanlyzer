"""
LLM Wrapper Module
Centralizes AI calls. Uses OpenAI if available, otherwise defaults to Pollinations.ai (Free).
"""

import os
import requests
import json
from config import APIKeys

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
        # Construct the prompt with system instruction embedded (Pollinations is raw text completion style usually, but handles chat context well via the openai endpoint)
        # Let's use their OpenAI compatible endpoint for structure
        
        headers = {'Content-Type': 'application/json'}
        payload = {
            "messages": [
                {"role": "system", "content": system_role},
                {"role": "user", "content": prompt}
            ],
            "model": "openai", # Requests a GPT-like model
            "jsonMode": False
        }
        
        # Pollinations OpenAI-compatible endpoint
        response = requests.post("https://text.pollinations.ai/", json=payload, timeout=30)
        
        if response.status_code == 200:
            # It returns the text directly usually
            return response.text
        else:
            return f"Error from AI Provider: {response.status_code}"
            
    except Exception as e:
        return f"AI Generation Failed: {str(e)}"

class AIEngine:
    @staticmethod
    def chat(prompt, system="You are an expert career coach."):
        return generate_text(prompt, system)

ai_engine = AIEngine()
