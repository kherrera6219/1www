import os
from flask import Flask, render_template, request, jsonify
from chatbot import get_chatbot_response, get_chatbot_info

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
        response = get_chatbot_response(user_message)
        return jsonify({'response': response})
    except Exception as e:
        app.logger.error(f"Error processing message: {str(e)}")
        return jsonify({'error': 'An error occurred while processing your request'}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
