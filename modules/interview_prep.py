"""
Interview Preparation Module
Features: Question Generator, Model Answers
"""

from utils.llm_wrapper import ai_engine
import json

class InterviewCoach:
    
    def generate_questions(self, role: str, skills: list, level: str = "Intermediate") -> list:
        """
        Generates interview questions based on role and skills.
        """
        skill_str = ", ".join(skills)
        prompt = f"""
        Generate 5 interview questions for a {level} {role} position.
        The candidate has these skills: {skill_str}.
        
        Include:
        - 2 Technical questions specific to the skills.
        - 2 Behavioral/Scenario questions.
        - 1 "Culture Fit" or Soft Skill question.
        
        Output format: Return ONLY a JSON list of strings.
        Example: ["Question 1", "Question 2"]
        """
        
        response = ai_engine.chat(prompt, system="You are a hiring manager. Output JSON only.")
        
        # Clean response to ensure list
        try:
            # Simple heuristic to extract list if wrapped in text
            if "[" in response and "]" in response:
                start = response.find("[")
                end = response.rfind("]") + 1
                return json.loads(response[start:end])
            return json.loads(response)
        except:
            return [
                f"Can you explain your experience with {skill_str}?",
                f"Tell me about a challenge you faced as a {role}.",
                "Where do you see yourself in 5 years?",
                "What is your greatest technical strength?",
                "How do you handle conflict in a team?"
            ]

    def get_model_answer(self, question: str) -> str:
        """
        Generates a model answer using the STAR method.
        """
        prompt = f"""
        Provide a model answer for this interview question: "{question}"
        Use the STAR method (Situation, Task, Action, Result) if applicable.
        Keep it under 150 words.
        """
        return ai_engine.chat(prompt, system="You are an interview coach.")

interview_coach = InterviewCoach()
