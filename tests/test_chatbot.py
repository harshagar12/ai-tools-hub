import pytest
from src.components.chatbot import get_gemini_response, chat_with_ai

def test_get_gemini_response():
    """Test basic response generation"""
    response = get_gemini_response("Hello, how are you?")
    assert isinstance(response, str)
    assert len(response) > 0

def test_chat_with_ai():
    """Test conversation context maintenance"""
    conversation_history = [
        {"user": "Hi, tell me a joke", "ai": "Why did the scarecrow win an award? Because he was outstanding in his field!"}
    ]
    response = chat_with_ai(conversation_history)
    assert isinstance(response, str)
    assert len(response) > 0