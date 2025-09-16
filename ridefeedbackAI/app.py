from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import requests

app = Flask(__name__)
CORS(app)

# Ollama Server Configuration
OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL_NAME = "llama3.2"

def chatbot_response(user_input):
    """
    Generates a friendly, conversational response for the taxi service chatbot.
    The assistant acts like a ride buddy and optimizes customer interaction.
    """
    try:
        prompt = f"""
        You are a friendly AI assistant for a taxi service. 
        Your goal is to chat with customers, answer their ride-related questions, 
        analyze their feedback, and make their experience delightful.

        - If the user greets you, respond warmly.
        - If they give feedback, summarize it, identify sentiment, and reply accordingly.
        - If they ask for help, provide a useful and friendly answer.
        - Keep responses short, natural, and engaging.
        - Maintain a casual and friendly tone, like a helpful travel companion.

        User: "{user_input}"
        AI:
        """

        payload = {
            "model": MODEL_NAME,
            "prompt": prompt,
            "stream": False,
            "options": {"temperature": 0.8, "max_tokens": 150}
        }

        response = requests.post(OLLAMA_URL, json=payload)
        if response.status_code == 200:
            return response.json().get("response", "Hmm, I'm not sure. Can you say that again?")
        return "Oops! Something went wrong."

    except Exception as e:
        print(f"Error: {e}")
        return "Sorry, I'm having trouble right now. Try again later."

@app.route("/")
def home():
    return render_template("index.html")  # Ensure you have an index.html UI

@app.route("/chat", methods=["POST"])
def chat():
    """Handles chatbot interactions for friendly conversations."""
    try:
        user_message = request.json.get("message", "").strip()
        if not user_message:
            return jsonify({"response": "Hey there! How can I help with your ride today? 😊"})

        bot_response = chatbot_response(user_message)
        return jsonify({"response": bot_response})

    except Exception as e:
        print(f"Error: {e}")
        return jsonify({"response": "Oops! Something went wrong. Let's try again!"})

if __name__ == "__main__":
    app.run(debug=True, port=5001)
 