# routes/chatbot_routes.py
from flask import Blueprint, request, jsonify,current_app
from chatbot.chatbot_service import ChatbotService
from chatbot.config import api_key
from chatbot.analysis_service import AnalysisService
from chatbot.track import get_emotion_history,get_chat_history
chatbot_bp = Blueprint("chatbot_bp", __name__)

# --- Initialization (same as your new app.py) ---
GEMINI_API_KEY = api_key
analysis_service = AnalysisService()

print(" Chatbot Service is ready to accept requests.")

# --- Chat Route ---
@chatbot_bp.route("/api/v1/chat", methods=["POST"])
def chat():
    users_collection = current_app.config["USERS_COLLECTION"]
    chat_collection = current_app.config["CHATS_COLLECTION"]
    
    chatbot_service = ChatbotService(
        users_collection=users_collection,
        chat_collection=chat_collection,
        analysis_service=analysis_service
    )
    data = request.get_json()
    u_id = data.get("user_id")
    message = data.get("message")

    if not u_id or not message:
        return jsonify({"error": "user_id and message are required"}), 400

    try:
        response_payload = chatbot_service.handle_chat_request(u_id, message)
        return jsonify(response_payload)
    except Exception as e:
        print(f"Chatbot Error: {e}")
        return jsonify({"error": "Internal Server Error"}), 500

@chatbot_bp.route("/api/v1/emotion-history", methods=["POST"])
def predicted():
    return get_emotion_history()

@chatbot_bp.route("/api/v1/allchats", methods=["POST"])
def chathistory():
    return get_chat_history()