import re
from functools import lru_cache

def filter_content(text):
    # Simple content filtering (can be expanded)
    inappropriate_words = ["offensive", "vulgar", "hate"]
    for word in inappropriate_words:
        if word in text.lower():
            return True
    return False

@lru_cache(maxsize=100)
def get_chatbot_response(user_input):
    # Convert user input to lowercase for case-insensitive matching
    user_input = user_input.lower()

    # Check for inappropriate content
    if filter_content(user_input):
        return "I'm sorry, but I can't respond to that kind of language or content."

    # Simple dictionary of predefined responses
    responses = {
        "hello": "Hello! I'm an AI chatbot. How can I assist you today?",
        "how are you": "As an AI, I don't have feelings, but I'm functioning well and ready to help you. How can I assist you?",
        "what's your name": "I'm an AI chatbot created to assist users. You can call me ChatBot.",
        "bye": "Goodbye! If you have any more questions in the future, feel free to ask.",
        "help": "I'm here to assist you with general questions. Please note that my knowledge is limited and I may not always have the most up-to-date information.",
    }
    
    # Check if the user input matches any predefined responses
    for key in responses:
        if key in user_input:
            return responses[key]
    
    # If no match is found, return a default response
    return "I'm sorry, I don't have enough information to answer that question accurately. Is there something else I can help you with?"

def get_chatbot_info():
    return {
        "name": "ChatBot",
        "type": "AI",
        "capabilities": [
            "Answering general questions",
            "Providing basic assistance",
        ],
        "limitations": [
            "Limited knowledge base",
            "No access to real-time information",
            "Unable to learn from conversations",
        ]
    }
