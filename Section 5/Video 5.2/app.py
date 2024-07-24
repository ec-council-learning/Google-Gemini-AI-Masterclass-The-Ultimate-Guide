from flask import Flask, request, jsonify, send_from_directory
from dotenv import load_dotenv
import os
import google.generativeai as genai
from flask_cors import CORS

# Load environment variables
load_dotenv()

app = Flask(__name__, static_folder='static')
CORS(app)

# Configure Google Gemini API
genai.configure(api_key=os.getenv("GCP_API_KEY"))
model = genai.GenerativeModel("gemini-pro")

@app.route('/')
def index():
    return send_from_directory(app.static_folder, 'index.html')

@app.route('/chat', methods=['POST'])
def chat():
    user_input = request.json.get("message")
    if not user_input:
        return jsonify({"error": "No message provided"}), 400

    chat_session = model.start_chat()
    prompt = f"You are a car expert. Keep your responses brief; one to two sentences at most. The user says: {user_input}"

    full_response = ""
    responses = chat_session.send_message(prompt, stream=True)
    for response in responses:
        full_response += response.text

    return jsonify({"response": full_response})

if __name__ == '__main__':
    app.run(debug=True)
