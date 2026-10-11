import os
from flask import Flask, jsonify, render_template, request
from chatbot import ChatbotEngine, load_intents

app = Flask(__name__)
app.config["MAX_CONTENT_LENGTH"] = 16 * 1024
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
engine = ChatbotEngine(load_intents(os.environ.get("INTENTS_PATH", os.path.join(BASE_DIR, "intents.json"))),
                       threshold=float(os.environ.get("CONFIDENCE_THRESHOLD", "0.52")))

@app.get("/")
def index():
    return render_template("index.html")

@app.get("/health")
def health():
    return jsonify({"status": "ok", "service": "smartassist-chatbot"})

@app.get("/api/intents")
def suggestions():
    return jsonify({"suggestions": [
        {"label": "Business hours", "message": "What are your business hours?"},
        {"label": "Pricing", "message": "How much does your service cost?"},
        {"label": "Contact support", "message": "How can I contact support?"},
        {"label": "Refund policy", "message": "What is your refund policy?"}
    ]})

@app.post("/api/chat")
def chat():
    payload = request.get_json(silent=True)
    if not isinstance(payload, dict):
        return jsonify({"error": "Send a JSON object containing a 'message' field."}), 400
    message = payload.get("message")
    if not isinstance(message, str):
        return jsonify({"error": "'message' must be a string."}), 400
    message = message.strip()
    if not message:
        return jsonify({"error": "Please enter a message."}), 400
    if len(message) > 1000:
        return jsonify({"error": "Message is too long. Please keep it under 1,000 characters."}), 413
    return jsonify(engine.respond(message))

@app.errorhandler(413)
def too_large(_error):
    return jsonify({"error": "Request is too large."}), 413

@app.errorhandler(404)
def not_found(_error):
    return jsonify({"error": "The requested resource was not found."}), 404

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=int(os.environ.get("PORT", "5000")), debug=False)
