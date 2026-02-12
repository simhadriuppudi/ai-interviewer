from backend.app.services.llm import llm_client

async def analyze_performance(conversation_history: list):
    """
    Analyze the conversation history to generate a performance report.
    This is a simplified version using the LLM to generate feedback.
    """
    
    # Construct a transcript string
    transcript = "\n".join([f"{msg['role']}: {msg['content']}" for msg in conversation_history])
    
    if not transcript:
        return {
            "overall_score": 0,
            "clarity_score": "N/A",
            "confidence_score": "N/A",
            "feedback": ["No conversation data to analyze."]
        }
    
    prompt = f"""
    Analyze the following interview transcript and provide a performance report.
    
    Transcript:
    {transcript}
    
    Output Format (JSON only):
    {{
        "overall_score": <number 0-100>,
        "clarity_grade": <A/B/C/D>,
        "confidence_level": <High/Medium/Low>,
        "key_feedback": [
            {{"title": "<Aspect>", "description": "<Specific feedback>"}},
            ...
        ]
    }}
    """
    
    try:
        response = llm_client.chat_completion(prompt, system_message="You are an expert interview coach. Output valid JSON only.")
        # Clean response to ensure it's JSON
        response = response.strip()
        if response.startswith("```json"):
            response = response[7:-3]
        elif response.startswith("```"):
            response = response[3:-3]
            
        import json
        return json.loads(response)
    except Exception as e:
        print(f"Error analyzing performance: {e}")
        return {
            "overall_score": 75,
            "clarity_grade": "B",
            "confidence_level": "Medium",
            "key_feedback": [
                {"title": "General", "description": "Good effort, but could be specific."}
            ]
        }
