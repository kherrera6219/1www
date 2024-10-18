import os
from flask import Flask, render_template, request, jsonify
from chatbot import get_chatbot_response, get_chatbot_info, classify_intent

app = Flask(__name__)
app.secret_key = os.environ.get("FLASK_SECRET_KEY") or "a secret key"

@app.route('/')
def index():
    chatbot_info = get_chatbot_info()
    return render_template('index.html', chatbot_info=chatbot_info)

@app.route('/get_response', methods=['POST'])
def get_response():
    user_message = request.form.get('message', '')
    if not user_message:
        return jsonify({'error': 'Empty message'}), 400

    try:
        response_data = get_chatbot_response(user_message)
        return jsonify(response_data)
    except Exception as e:
        app.logger.error(f"Error processing message: {str(e)}")
        return jsonify({'error': 'An error occurred while processing your request'}), 500

@app.route('/demo')
def demo():
    sample_messages = [
        "Hello, how are you?",
        "What's the weather like today?",
        "Tell me a joke",
        "Who created you?",
        "Thank you for your help",
        "I'm feeling sad today",
        "What time is it?",
        "You're doing a great job!",
        "Sorry, I didn't understand that",
        "Can you help me with something?"
    ]
    demo_responses = []
    for message in sample_messages:
        response_data = get_chatbot_response(message)
        demo_responses.append({'message': message, **response_data})
    return render_template('demo.html', demo_responses=demo_responses)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
