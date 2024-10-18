import re
from functools import lru_cache
import spacy
import os
from textblob import TextBlob
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import google.generativeai as genai

# Download spaCy model if not already present
if not spacy.util.is_package("en_core_web_sm"):
    spacy.cli.download("en_core_web_sm")

nlp = spacy.load("en_core_web_sm")

# Initialize TF-IDF vectorizer
vectorizer = TfidfVectorizer()

# Configure Google Generative AI
genai.configure(api_key=os.environ['GOOGLE_AI_API_KEY'])
model = genai.GenerativeModel('gemini-pro')

# Enhanced intents and responses
intents = {
    "greeting": ["hello", "hi", "hey", "greetings", "good morning", "good afternoon", "good evening"],
    "farewell": ["bye", "goodbye", "see you", "farewell", "take care"],
    "help": ["help", "assistance", "support", "guide", "how to"],
    "about": ["who are you", "what are you", "tell me about yourself", "your purpose"],
    "weather": ["weather", "forecast", "temperature", "rain", "sunny"],
    "time": ["time", "current time", "what time is it", "clock"],
    "gratitude": ["thanks", "thank you", "appreciate it", "grateful"],
    "apology": ["sorry", "apologize", "my mistake", "apologies"],
    "joke": ["tell me a joke", "joke", "funny", "make me laugh"],
    "compliment": ["you're great", "you're smart", "well done", "good job"],
}

responses = {
    "greeting": ["Hello! I'm an AI chatbot. How can I assist you today?", "Hi there! What can I help you with?", "Greetings! How may I be of service?"],
    "farewell": ["Goodbye! If you have any more questions in the future, feel free to ask.", "Take care! Don't hesitate to return if you need further assistance.", "Farewell! I hope our interaction was helpful."],
    "help": ["I'm here to assist you with general questions. What specific area do you need help with?", "I'd be happy to help! Could you please provide more details about what you need assistance with?"],
    "about": ["I'm an AI chatbot created to assist users with various queries. My knowledge is based on the data I was trained on, and I'm constantly learning to provide better assistance.", "As an AI assistant, I'm designed to help with a wide range of topics. I don't have personal experiences, but I can provide information and answer questions to the best of my abilities."],
    "weather": ["I'm sorry, I don't have access to real-time weather information. You might want to check a weather website or app for the most up-to-date forecast.", "While I can't provide current weather data, I can suggest some reliable weather services if you'd like."],
    "time": ["I'm afraid I don't have access to the current time. You can check your device's clock for the accurate time.", "As an AI, I don't have a sense of time, but I recommend checking your local time display for the most accurate information."],
    "gratitude": ["You're welcome! I'm glad I could help.", "It's my pleasure to assist you!", "I'm happy to be of service!"],
    "apology": ["No need to apologize. I'm here to help!", "It's alright, everyone makes mistakes. How can I assist you further?", "No worries at all. Let's move forward - what can I help you with?"],
    "joke": ["Why don't scientists trust atoms? Because they make up everything!", "What do you call a fake noodle? An impasta!", "Why did the scarecrow win an award? He was outstanding in his field!"],
    "compliment": ["Thank you for the kind words! I'm just doing my best to assist.", "I appreciate your compliment! I'm glad I could meet your expectations.", "That's very kind of you to say. I'm here to help in any way I can."],
}

# Prepare the vectorizer
corpus = [" ".join(intent) for intent in intents.values()]
vectorizer.fit(corpus)

def filter_content(text):
    # Simple content filtering (can be expanded)
    inappropriate_words = ["offensive", "vulgar", "hate"]
    for word in inappropriate_words:
        if word in text.lower():
            return True
    return False

def classify_intent(user_input):
    user_vector = vectorizer.transform([user_input.lower()])
    similarities = cosine_similarity(user_vector, vectorizer.transform(corpus))
    max_similarity = similarities.max()
    if max_similarity > 0.3:  # Threshold for intent matching
        intent_index = similarities.argmax()
        return list(intents.keys())[intent_index]
    return None

def extract_entities(doc):
    entities = []
    for ent in doc.ents:
        entities.append({
            "text": ent.text,
            "label": ent.label_,
            "start": ent.start_char,
            "end": ent.end_char
        })
    return entities

def extract_noun_phrases(doc):
    return [{"text": chunk.text, "root": chunk.root.text} for chunk in doc.noun_chunks]

def analyze_sentiment(text):
    blob = TextBlob(text)
    return {
        "polarity": blob.sentiment.polarity,
        "subjectivity": blob.sentiment.subjectivity
    }

class ConversationContext:
    def __init__(self):
        self.context = {}
        self.history = []

    def update(self, user_input, response, intent, entities, noun_phrases, sentiment):
        self.history.append({"user": user_input, "bot": response})
        self.context["last_intent"] = intent
        self.context["entities"] = entities
        self.context["noun_phrases"] = noun_phrases
        self.context["sentiment"] = sentiment

    def get_context(self):
        return self.context

    def get_history(self):
        return self.history[-5:]  # Return last 5 interactions

conversation_context = ConversationContext()

@lru_cache(maxsize=100)
def get_chatbot_response(user_input):
    # Check for inappropriate content
    if filter_content(user_input):
        return {"response": "I'm sorry, but I can't respond to that kind of language or content."}

    # Process user input with spaCy
    doc = nlp(user_input)

    # Classify intent
    intent = classify_intent(user_input)

    # Extract named entities
    entities = extract_entities(doc)

    # Extract noun phrases
    noun_phrases = extract_noun_phrases(doc)

    # Perform sentiment analysis
    sentiment = analyze_sentiment(user_input)

    # Get conversation context
    context = conversation_context.get_context()

    # Prepare prompt for Gemini Pro
    prompt = f"""
    User input: {user_input}
    Intent: {intent if intent else 'Unknown'}
    Entities: {', '.join([e['text'] for e in entities]) if entities else 'None'}
    Noun phrases: {', '.join([np['text'] for np in noun_phrases]) if noun_phrases else 'None'}
    Sentiment: Polarity {sentiment['polarity']:.2f}, Subjectivity {sentiment['subjectivity']:.2f}
    
    Previous context: {context}
    
    Based on this information, provide a helpful and context-aware response:
    """

    try:
        # Generate response using Gemini Pro
        gemini_response = model.generate_content(prompt)
        response = gemini_response.text
    except Exception as e:
        print(f"Error generating response from Gemini Pro: {str(e)}")
        # Fallback to intent-based response
        if intent and intent in responses:
            response = responses[intent][0]
        else:
            response = "I apologize, but I'm having trouble generating a response at the moment. Could you please rephrase your question?"

    # Update conversation context
    conversation_context.update(user_input, response, intent, entities, noun_phrases, sentiment)

    return {
        "response": response,
        "intent": intent,
        "entities": entities,
        "noun_phrases": noun_phrases,
        "sentiment": sentiment
    }

def get_chatbot_info():
    return {
        "name": "ChatBot",
        "type": "AI",
        "capabilities": [
            "Answering general questions",
            "Providing basic assistance",
            "Natural language processing",
            "Intent classification",
            "Entity recognition",
            "Noun phrase extraction",
            "Sentiment analysis",
            "Context-aware responses",
            "Advanced language generation using Gemini Pro"
        ],
        "limitations": [
            "Limited knowledge base",
            "No access to real-time information",
            "Unable to learn from conversations",
            "May not understand complex or ambiguous queries",
            "Dependent on external AI service (Gemini Pro) for advanced responses"
        ]
    }
