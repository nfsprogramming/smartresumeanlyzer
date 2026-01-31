"""
Mock Interview Module
"""

from utils.llm_wrapper import ai_engine

class MockInterviewer:
    def get_response(self, history: list, user_input: str) -> str:
        """
        Chat with the user acting as an interviewer.
        """
        # Format history for prompt
        # History is likely `[{"role": "user", "content": ...}, ...]`
        
        conversation_text = ""
        for msg in history[-5:]: # Keep last 5 turns for context window
            conversation_text += f"{msg['role'].upper()}: {msg['content']}\n"
            
        prompt = f"""
        Current Conversation:
        {conversation_text}
        USER: {user_input}
        
        Respond as the Interviewer. Be professional but conversational. Ask a follow-up question.
        Stay in character. Do not repeat "User:" or "Interviewer:" prefixes in your output.
        """
        
        return ai_engine.chat(prompt, system="You are a professional hiring manager conducting an interview.")

mock_interviewer = MockInterviewer()
