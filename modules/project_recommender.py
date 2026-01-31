"""
Smart Project Recommendation Engine
Uses AI to generate unique, tailored project ideas based on missing skills.
"""

from typing import List, Dict
import json
from utils.llm_wrapper import ai_engine

class ProjectRecommender:
    """
    AI-powered Project Brainstormer.
    """
    
    def get_recommendations(self, missing_skills: List[str]) -> List[Dict]:
        """
        Ask AI for project ideas that incorporate these skills.
        """
        skills_str = ", ".join(missing_skills)
        
        prompt = f"""
        Generate 5 unique and impressive portfolio project ideas that would help a developer learn these specific skills: {skills_str}.
        
        Requirements:
        1. Projects should be non-trivial (Intermediate to Advanced).
        2. Must include the specific missing skills in the tech stack.
        3. Avoid generic to-do lists. Suggest things like "Real-time Dashboard", "AI-powered CRM", "Decentralized Voting App", etc.
        
        Output Format:
        Return ONLY a JSON list of objects with these keys: "name", "description", "difficulty", "skills" (list of strings).
        
        Example:
        [
            {{"name": "Crypto Arbitrage Bot", "description": "...", "difficulty": "Advanced", "skills": ["Python", "Web3"]}}
        ]
        """
        
        response = ai_engine.chat(prompt, system="You are a Senior Engineering Manager mentoring a junior. Return JSON only.")
        
        # Robust JSON Parsing
        try:
            # Find JSON brackets in case of extra text
            start = response.find("[")
            end = response.rfind("]") + 1
            if start != -1 and end != -1:
                json_str = response[start:end]
                return json.loads(json_str)
            else:
                return self._fallback_ideas(missing_skills)
        except Exception as e:
            print(f"Project Gen Error: {e}")
            return self._fallback_ideas(missing_skills)
            
    def _fallback_ideas(self, skills) -> List[Dict]:
        """Return static ideas if AI fails."""
        return [
            {
                "name": "Full Stack Analytics Dashboard",
                "difficulty": "Intermediate",
                "description": "Build a dashboard visualizing data from a public API.",
                "skills": skills + ["React", "D3.js"]
            },
            {
                "name": "Real-time Chat Application",
                "difficulty": "Advanced",
                "description": "A websocket-based chat app with end-to-end encryption.",
                "skills": skills + ["Socket.io", "Redis"]
            },
             {
                "name": "AI Content Generator",
                "difficulty": "Intermediate",
                "description": "A tool that uses OpenAI/Gemini to write blog posts.",
                "skills": skills + ["Python", "API Integration"]
            }
        ]

project_recommender = ProjectRecommender()
