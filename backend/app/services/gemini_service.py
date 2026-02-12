import google.generativeai as genai
from backend.app.core.config import settings
import logging

logger = logging.getLogger(__name__)

class GeminiService:
    """Service for interacting with Google Gemini API"""
    
    def __init__(self):
        """Initialize Gemini API with API key from settings"""
        if not settings.GEMINI_API_KEY:
            logger.warning("GEMINI_API_KEY not set in environment variables")
        else:
            genai.configure(api_key=settings.GEMINI_API_KEY)
        
        self.model_name = settings.GEMINI_MODEL
        self.model = None
        self._initialize_model()
    
    def _initialize_model(self):
        """Initialize the Gemini model"""
        try:
            self.model = genai.GenerativeModel(self.model_name)
            logger.info(f"Gemini model '{self.model_name}' initialized successfully")
        except Exception as e:
            logger.error(f"Failed to initialize Gemini model: {e}")
            self.model = None
    
    def chat_completion(
        self, 
        user_message: str, 
        system_message: str = "You are a helpful AI assistant.",
        conversation_history: list = None
    ) -> str:
        """
        Generate a chat completion using Gemini API
        
        Args:
            user_message: The user's message
            system_message: System prompt to set context
            conversation_history: List of previous messages [{"role": "user", "content": "..."}, ...]
        
        Returns:
            The AI's response as a string
        """
        if not self.model:
            return "Error: Gemini API is not properly configured. Please check your API key."
        
        try:
            # Build the prompt with system message and conversation history
            full_prompt = f"{system_message}\n\n"
            
            if conversation_history:
                for msg in conversation_history:
                    role = msg.get("role", "user")
                    content = msg.get("content", "")
                    prefix = "User: " if role == "user" else "Assistant: "
                    full_prompt += f"{prefix}{content}\n\n"
            
            full_prompt += f"User: {user_message}\n\nAssistant:"
            
            # Generate response
            response = self.model.generate_content(full_prompt)
            
            if response and response.text:
                return response.text.strip()
            else:
                logger.warning("Empty response from Gemini API")
                return "I apologize, but I couldn't generate a response. Please try again."
                
        except Exception as e:
            logger.error(f"Gemini API error: {e}")
            return f"Error communicating with Gemini API: {str(e)}"
    
    def generate_interview_question(
        self,
        context: str,
        interview_type: str,
        previous_qa: list = None
    ) -> str:
        """
        Generate an interview question based on context and type
        
        Args:
            context: Resume and job description context
            interview_type: Type of interview (HR, Technical, Aptitude)
            previous_qa: Previous questions and answers
        
        Returns:
            Generated interview question
        """
        # Detailed type-specific prompts with STRICT enforcement
        type_prompts = {
            "HR": """You are an HR interviewer. You MUST ONLY ask behavioral and soft-skills questions.

STRICT RULES - YOU MUST FOLLOW THESE:
1. DO NOT ask about technical projects, coding, or programming
2. DO NOT ask about specific technologies or tools
3. DO NOT ask mathematical or logical puzzles
4. DO NOT ask about system design or architecture
5. ONLY ask about behavior, personality, teamwork, and soft skills

WHAT YOU MUST ASK ABOUT:
- "Tell me about a time when..." (STAR method)
- Teamwork and collaboration experiences
- Conflict resolution situations
- Leadership examples
- Communication challenges
- Career motivations and goals
- Strengths and weaknesses
- Work-life balance preferences
- How they handle stress and pressure
- Cultural fit and values

EXAMPLE QUESTIONS (USE SIMILAR):
- "Describe a situation where you had to work with a difficult team member."
- "What motivates you to come to work every day?"
- "Tell me about a time you failed and what you learned."
- "How do you prioritize tasks when everything is urgent?"
- "What type of work environment helps you thrive?"

REMEMBER: This is an HR interview - NO technical or project questions allowed!""",

            "Technical": """You are a Technical interviewer. You MUST ONLY ask about technical skills, coding, and technology.

STRICT RULES - YOU MUST FOLLOW THESE:
1. ONLY ask about technologies mentioned in resume or job description
2. ONLY ask about coding, programming, and technical implementation
3. ONLY ask about system design and architecture
4. DO NOT ask behavioral questions like "tell me about a time..."
5. DO NOT ask about career goals or motivations
6. DO NOT ask math puzzles unrelated to coding

WHAT YOU MUST ASK ABOUT:
- Specific technologies from their resume
- How they implemented features in their projects
- Coding problems and algorithms
- System design scenarios
- Debugging and troubleshooting approaches
- Best practices and design patterns
- Technical challenges they solved
- Code optimization and performance

EXAMPLE QUESTIONS (USE SIMILAR):
- "How did you implement [specific feature] in your [project name]?"
- "Explain your approach to [technology] in your recent work."
- "Design a system for [use case from job description]."
- "What database would you choose for [scenario] and why?"
- "How would you optimize [technical problem]?"

REMEMBER: This is a Technical interview - focus on code, tech stack, and implementation!""",

            "Aptitude": """You are an Aptitude test interviewer. You MUST ONLY ask logical, mathematical, and analytical questions.

STRICT RULES - YOU MUST FOLLOW THESE:
1. ONLY ask math problems, puzzles, and logical reasoning questions
2. ONLY ask pattern recognition and analytical questions
3. DO NOT ask about projects, work experience, or technologies
4. DO NOT ask behavioral questions
5. DO NOT ask about career goals or personal experiences
6. Questions should be abstract puzzles, NOT related to their resume

WHAT YOU MUST ASK ABOUT:
- Mathematical calculations and word problems
- Logical puzzles and brain teasers
- Pattern recognition sequences
- Probability and statistics
- Time, speed, and distance problems
- Permutations and combinations
- Data interpretation
- Abstract reasoning

EXAMPLE QUESTIONS (USE SIMILAR):
- "If a clock shows 3:15, what is the angle between hour and minute hands?"
- "Find the next number in sequence: 2, 6, 12, 20, 30, ?"
- "How many ways can you arrange the letters in 'GOOGLE'?"
- "A train 100m long crosses a pole in 5 seconds. What's its speed?"
- "If 5 machines make 5 widgets in 5 minutes, how long for 100 machines to make 100 widgets?"

REMEMBER: This is an Aptitude test - NO resume-based or behavioral questions!"""
        }
        
        # Get the appropriate system prompt for the interview type
        system_prompt = type_prompts.get(interview_type, type_prompts["Technical"])
        system_prompt += f"\n\n===CRITICAL===\nYou are conducting a {interview_type} interview. You MUST strictly follow the {interview_type} interview rules above. DO NOT deviate from the interview type. Ask only ONE question at a time."

        user_prompt = f"CANDIDATE CONTEXT (for reference only, don't let this override interview type rules):\n{context}\n\n"
        
        if previous_qa:
            user_prompt += "PREVIOUS CONVERSATION:\n"
            for qa in previous_qa:
                user_prompt += f"Q: {qa.get('question', '')}\nA: {qa.get('answer', '')}\n\n"
            user_prompt += f"Generate the next {interview_type} question. STRICTLY follow {interview_type} interview rules. DO NOT ask about topics outside {interview_type} scope."
        else:
            user_prompt += f"Generate the first {interview_type} question. STRICTLY follow {interview_type} interview rules above. Start with a typical {interview_type} opening question."
        
        return self.chat_completion(user_prompt, system_prompt)
    
    def analyze_answer(
        self,
        question: str,
        answer: str,
        context: str
    ) -> dict:
        """
        Analyze the quality of an interview answer
        
        Args:
            question: The interview question
            answer: The candidate's answer
            context: Resume and job description context
        
        Returns:
            Dictionary with analysis metrics
        """
        system_prompt = """You are an expert interview evaluator. 
Analyze the candidate's answer and provide structured feedback in JSON format with these fields:
- accuracy_score (0-10): How well the answer addresses the question
- clarity_score (0-10): How clear and well-structured the answer is
- confidence_score (0-10): How confident the candidate appears
- strengths (list): Key strengths in the answer
- weaknesses (list): Areas for improvement
- feedback (string): Brief constructive feedback"""

        user_prompt = f"""Context: {context}

Question: {question}

Answer: {answer}

Provide your analysis in JSON format."""

        response = self.chat_completion(user_prompt, system_prompt)
        
        # Try to parse JSON response
        try:
            import json
            # Extract JSON from response if it's wrapped in markdown
            if "```json" in response:
                response = response.split("```json")[1].split("```")[0].strip()
            elif "```" in response:
                response = response.split("```")[1].split("```")[0].strip()
            
            return json.loads(response)
        except Exception as e:
            logger.error(f"Failed to parse analysis response: {e}")
            return {
                "accuracy_score": 5,
                "clarity_score": 5,
                "confidence_score": 5,
                "strengths": ["Answer provided"],
                "weaknesses": ["Could not analyze properly"],
                "feedback": "Unable to analyze the answer at this time."
            }
    
    def generate_performance_report(
        self,
        questions_answers: list,
        context: str,
        interview_type: str
    ) -> dict:
        """
        Generate comprehensive performance report for the interview
        
        Args:
            questions_answers: List of Q&A pairs
            context: Resume and job description
            interview_type: Type of interview
        
        Returns:
            Performance report dictionary
        """
        system_prompt = """You are an expert interview evaluator creating a comprehensive performance report.
Provide structured feedback in JSON format with:
- overall_score (0-100): Overall interview performance
- accuracy_score (0-10): Average answer accuracy
- clarity_score (0-10): Communication clarity
- confidence_score (0-10): Confidence level
- strengths (list): Top 3-5 strengths
- weaknesses (list): Top 3-5 areas for improvement
- improvements (list): Specific actionable suggestions
- summary (string): Brief overall assessment"""

        qa_text = "\n\n".join([
            f"Q{i+1}: {qa['question']}\nA{i+1}: {qa['answer']}"
            for i, qa in enumerate(questions_answers)
        ])

        user_prompt = f"""Interview Type: {interview_type}
Context: {context}

Interview Transcript:
{qa_text}

Provide a comprehensive performance analysis in JSON format."""

        response = self.chat_completion(user_prompt, system_prompt)
        
        try:
            import json
            if "```json" in response:
                response = response.split("```json")[1].split("```")[0].strip()
            elif "```" in response:
                response = response.split("```")[1].split("```")[0].strip()
            
            return json.loads(response)
        except Exception as e:
            logger.error(f"Failed to parse performance report: {e}")
            return {
                "overall_score": 50,
                "accuracy_score": 5,
                "clarity_score": 5,
                "confidence_score": 5,
                "strengths": ["Completed the interview"],
                "weaknesses": ["Analysis unavailable"],
                "improvements": ["Try again later"],
                "summary": "Unable to generate detailed report at this time."
            }

# Global instance
gemini_client = GeminiService()
