import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()

def get_gemini_response(question):
    """Generate response using Google Gemini API"""
    try:
        genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
        model = genai.GenerativeModel("gemini-pro")
        response = model.generate_content(question)
        return response.text
    except Exception as e:
        return f"Error generating response: {str(e)}"

def chat_with_ai(conversation_history=None):
    """Maintain conversation context and generate responses"""
    if conversation_history is None:
        conversation_history = []
    
    model = genai.GenerativeModel("gemini-pro")
    
    try:
        if conversation_history:
            # Create a context-aware prompt
            context = "\n".join([f"User: {msg['user']}\nAI: {msg['ai']}" for msg in conversation_history])
            full_prompt = f"{context}\nUser's latest message:"
        
        return model.generate_content(full_prompt).text
    except Exception as e:
        return f"Conversation error: {str(e)}"