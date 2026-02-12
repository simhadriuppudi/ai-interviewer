"""
LLM Service - Wrapper around Gemini for backward compatibility
"""
from backend.app.services.gemini_service import gemini_client

class LLMService:
    """Wrapper around Gemini service for backward compatibility"""
    
    def __init__(self):
        self.gemini = gemini_client
    
    def chat_completion(self, user_message: str, system_message: str = "You are a helpful assistant.") -> str:
        """
        Chat completion using Gemini API
        
        Args:
            user_message: The user's message
            system_message: System prompt to set context
        
        Returns:
            The AI's response as a string
        """
        try:
            return self.gemini.chat_completion(user_message, system_message)
        except Exception as e:
            print(f"LLM Chat Error: {e}")
            return "I'm having trouble generating a response. Please try again."

# Global instance
llm_client = LLMService()
