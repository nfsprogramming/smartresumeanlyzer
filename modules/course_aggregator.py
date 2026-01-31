"""
Course Aggregator Module
Uses AI to curate specific high-quality learning resources with robust error handling.
"""

import streamlit as st
import json
from utils.llm_wrapper import ai_engine

class CourseAggregator:
    """
    AI-powered Learning Roadmap Curator.
    """
    
    def get_learning_path(self, skills: list) -> dict:
        """
        Generates a roadmap for specific skills using AI.
        """
        if not skills:
            return {}
            
        skills_str = ", ".join(skills)
        prompt = f"""
        For each of these skills: {skills_str}, provide exactly 2 high-quality FREE learning resources.
        
        Output Format (STRICT JSON):
        {{
            "SkillName": [
                {{"title": "Resource Title", "url": "https://...", "platform": "YouTube", "type": "Video"}},
                {{"title": "Resource Title", "url": "https://...", "platform": "Docs", "type": "Article"}}
            ]
        }}
        
        Note: The value MUST be a LIST of objects.
        """
        
        response = ai_engine.chat(prompt, system="You are an expert technical mentor. Return ONLY clean JSON.")
        
        try:
            start = response.find("{")
            end = response.rfind("}") + 1
            if start != -1 and end != -1:
                data = json.loads(response[start:end])
                
                # Validation: Ensure values are lists
                validated_data = {}
                for k, v in data.items():
                    if isinstance(v, list):
                        validated_data[k] = v
                    elif isinstance(v, dict):
                        validated_data[k] = [v] # Wrap single dict in list
                return validated_data
                
            return self._fallback(skills)
        except:
            return self._fallback(skills)

    def _fallback(self, skills) -> dict:
        roadmap = {}
        for s in skills:
            roadmap[s] = [
                {"title": f"Learn {s} (YouTube)", "url": f"https://www.youtube.com/results?search_query=learn+{s}", "platform": "YouTube", "type": "Video"},
                {"title": f"{s} Documentation", "url": "https://google.com/search?q=" + s + "+docs", "platform": "Web", "type": "Article"}
            ]
        return roadmap

course_aggregator = CourseAggregator()
