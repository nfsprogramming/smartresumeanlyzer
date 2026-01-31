"""
Resume Authenticity Checker Module
Detects potential exaggerations, skill inflation, and inconsistencies
"""

import re
from datetime import datetime

class AuthenticityChecker:
    """
    Analyzes resume for potential red flags and authenticity issues.
    """
    
    def analyze_claims(self, resume_text: str) -> dict:
        """
        Analyze the resume for potential issues.
        Returns: { 'score': 0-100, 'flags': ['Flag 1', ...], 'details': ... }
        """
        flags = []
        score = 100
        
        # 1. Buzzword Overload
        buzzwords = ["visionary", "ninja", "rockstar", "guru", "world-class", "expert", "master"]
        buzz_count = 0
        for b in buzzwords:
            if re.search(r"\b" + re.escape(b) + r"\b", resume_text, re.IGNORECASE):
                buzz_count += 1
                
        if buzz_count > 3:
            flags.append(f"High usage of subjective buzzwords ({buzz_count} found). Focus on concrete achievements.")
            score -= 5

        # 2. Impossible Timelines (Heuristic)
        # e.g., "10 years experience in Swift" (Swift released 2014, so by 2026 it's 12 years. Wait, logic check.)
        # Let's use a known recent tech list.
        current_year = datetime.now().year
        tech_release_years = {
            "swift": 2014,
            "kubernetes": 2014,
            "react": 2013,
            "flutter": 2017,
            "chatgpt": 2022,
            "generative ai": 2020 # roughly
        }
        
        text_lower = resume_text.lower()
        for tech, year in tech_release_years.items():
            # Look for "X years in Tech"
            # Pattern: "(\d+) years.*tech" or "tech.*(\d+) years"
            
            # Simple check: 
            matches = re.findall(fr"(\d+)\+?\s*years?.*{tech}", text_lower)
            if not matches:
                 matches = re.findall(fr"{tech}.*?(\d+)\+?\s*years?", text_lower)
            
            for m in matches:
                try:
                    claimed_years = int(m)
                    max_possible = current_year - year + 1 # +1 buffer
                    if claimed_years > max_possible:
                        flags.append(f"Suspicious Claim: {claimed_years} years in '{tech}' (Technology released in {year}).")
                        score -= 15
                except:
                    pass

        # 3. Quantifiable Metrics Check
        # If resume has very few numbers, it might be vague
        numbers = re.findall(r"\d+[%]?", resume_text)
        if len(numbers) < 5:
            flags.append("Low density of quantifiable metrics. Hard to verify impact without numbers.")
            score -= 10
            
        # 4. "Result" keywords check
        result_words = ["resulted in", "led to", "increased by", "reduced by", "saved"]
        result_count = sum(1 for w in result_words if w in text_lower)
        if result_count < 2:
            flags.append("Lack of result-oriented language. Focus is too much on duties rather than outcomes.")
            score -= 5
            
        return {
            "score": max(0, score),
            "flags": flags,
            "verdict": "Likely Authentic" if score > 85 else "Needs Review" if score > 60 else "High Risk of Exaggeration"
        }

authenticity_checker = AuthenticityChecker()
