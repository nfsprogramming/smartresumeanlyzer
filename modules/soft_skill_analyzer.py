"""
Soft Skill Analyzer Module
Detects evidence of soft skills through language analysis
"""

import re
from textblob import TextBlob
from typing import Dict, List

class SoftSkillAnalyzer:
    """
    Analyzes text for soft skill indicators.
    """
    
    SOFT_SKILL_MAP = {
        "Leadership": ["led", "managed", "spearheaded", "mentored", "directed", "supervised", "orchestrated", "delegated"],
        "Teamwork": ["collaborated", "partnered", "assisted", "supported", "co-created", "brainstormed", "team"],
        "Communication": ["presented", "negotiated", "authored", "documented", "communicated", "proposed", "facilitated"],
        "Problem Solving": ["resolved", "solved", "debugged", "troubleshot", "optimized", "fixed", "diagnosed", "analyzed"],
        "Adaptability": ["learned", "adapted", "pivoted", "flexible", "adjusted", "transitioned"]
    }
    
    def analyze(self, text: str) -> Dict:
        """
        Analyze resume for soft skills and tone.
        """
        text_lower = text.lower()
        results = {}
        
        # 1. Skill Detection
        for category, keywords in self.SOFT_SKILL_MAP.items():
            count = 0
            evidence = []
            for kw in keywords:
                # Basic matching
                matches = re.findall(r"\b" + re.escape(kw) + r"\w*", text_lower)
                if matches:
                    count += len(matches)
                    evidence.append(kw)
            
            score = min(100, count * 15) # Simple scoring
            results[category] = {
                "score": score,
                "evidence": list(set(evidence)),
                "level": "High" if score > 60 else "Medium" if score > 30 else "Low"
            }
            
        # 2. Tone Analysis (Sentiment/Subjectivity)
        blob = TextBlob(text)
        sentiment = blob.sentiment.polarity # -1 to 1
        subjectivity = blob.sentiment.subjectivity # 0 to 1
        
        tone = "Neutral"
        if sentiment > 0.3: tone = "Positive/Enthusiastic"
        elif sentiment < -0.1: tone = "Negative/Critical" # Unlikely in resume
        
        style = "Objective" if subjectivity < 0.3 else "Subjective/Opinionated" if subjectivity > 0.6 else "Balanced"
        
        results["ToneAnalysis"] = {
            "Sentiment": tone,
            "Style": style,
            "RawSentiment": round(sentiment, 2),
            "RawSubjectivity": round(subjectivity, 2)
        }
        
        return results

soft_skill_analyzer = SoftSkillAnalyzer()
