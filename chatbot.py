def get_chatbot_response(user_input):
    # Simple dictionary of predefined responses
    responses = {
        "hello": "Hello! How can I help you today?",
        "how are you": "I'm doing well, thank you for asking. How about you?",
        "what's your name": "I'm a simple chatbot. You can call me ChatBot.",
        "bye": "Goodbye! Have a great day!",
    }
    
    # Convert user input to lowercase for case-insensitive matching
    user_input = user_input.lower()
    
    # Check if the user input matches any predefined responses
    for key in responses:
        if key in user_input:
            return responses[key]
    
    # If no match is found, return a default response
    return "I'm sorry, I don't understand. Can you please rephrase or ask something else?"
