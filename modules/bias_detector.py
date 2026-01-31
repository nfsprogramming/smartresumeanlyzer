"""
Bias Detector Module
Checks for gendered or exclusionary language
"""

import re

class BiasDetector:
    """
    Analyzes text for unconscious bias.
    """
    
    # Dictionary of potentially biased terms
    GENDER_CODED_MASCULINE = [
        "ninja", "rockstar", "guru", "hacker", "dominate", "decisive", 
        "competitive", "assertive", "strong", "aggressive"
    ]
    
    GENDER_CODED_FEMININE = [
        "dedicated", "supportive", "responsible", "cooperative", 
        "understanding", "dependency", "loyal"
    ]
    
    def analyze_bias(self, text: str) -> dict:
        """
        Check for biased language.
        """
        text_lower = text.lower()
        findings = []
        score = 100
        
        # Check Masculine Coded
        masc_found = [w for w in self.GENDER_CODED_MASCULINE if re.search(r"\b" + w + r"\b", text_lower)]
        if masc_found:
            findings.append({
                "type": "Masculine-Coded",
                "words": masc_found,
                "msg": "High usage of masculine-coded words can alienate some recruiters or signal aggressive culture fit."
            })
            score -= 5 * len(masc_found)
            
        # Check Feminine Coded (Usually not negative, but imbalance matters)
        fem_found = [w for w in self.GENDER_CODED_FEMININE if re.search(r"\b" + w + r"\b", text_lower)]
        if fem_found:
            findings.append({
                "type": "Feminine-Coded",
                "words": fem_found,
                "msg": "Heavy usage of these terms might soften your impact. Ensure you balance with 'Action' verbs."
            })
            
        # Ageism Check
        if re.search(r"\b(19\d{2})\b", text_lower): # Dates like 1990, 1985
             findings.append({
                "type": "Potential Ageism",
                "words": ["Dates pre-2000"],
                "msg": "Listing graduation dates or work dates older than 15 years can trigger unconscious age bias."
            })
             score -= 5
             
        return {
            "score": max(0, score),
            "findings": findings
        }

bias_detector = BiasDetector()
