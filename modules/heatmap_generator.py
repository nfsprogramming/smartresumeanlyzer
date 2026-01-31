"""
Heatmap Generator Module
Visualizes resume strength across different dimensions
"""

import pandas as pd
import re

class HeatmapGenerator:
    """
    Generates data for resume visualization.
    """
    
    def generate_section_analysis(self, text: str) -> pd.DataFrame:
        """
        Break down text into sections and analyze each.
        """
        # Heuristic section splitting
        sections = {
            "Summary": "",
            "Experience": "",
            "Education": "",
            "Skills": "",
            "Projects": ""
        }
        
        lower_text = text.lower()
        lines = text.split('\n')
        
        current_section = "Other"
        
        # Simple parser
        for line in lines:
            l = line.strip().lower()
            if "summary" in l or "profile" in l or "objective" in l:
                current_section = "Summary"
            elif "experience" in l or "employment" in l or "work history" in l:
                current_section = "Experience"
            elif "education" in l or "academic" in l:
                current_section = "Education"
            elif "skills" in l or "technologies" in l:
                current_section = "Skills"
            elif "project" in l:
                current_section = "Projects"
            
            if current_section in sections:
                sections[current_section] += line + " "
                
        # Analyze each section
        data = []
        for sec, content in sections.items():
            word_count = len(content.split())
            action_verbs = len([w for w in content.split() if w.endswith('ed')]) # Simple proxy
            numbers = len(re.findall(r"\d+", content))
            
            # Impact Score (Heuristic)
            impact = min(100, (action_verbs * 2 + numbers * 3))
            if word_count == 0: impact = 0
            
            data.append({
                "Section": sec,
                "Word Count": word_count,
                "Action Density": round((action_verbs/word_count)*100, 1) if word_count else 0,
                "Quantifiable Data": numbers,
                "Strength Score": impact
            })
            
        return pd.DataFrame(data)

heatmap_generator = HeatmapGenerator()
