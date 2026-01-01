""" # app.py
from flask import Flask, request, jsonify, current_app
from pymongo import MongoClient
from chatbot_service import ChatbotService
from config import api_key
from analysis_service import AnalysisService

app = Flask(__name__)
try:
    GEMINI_API_KEY = api_key
    analysis_service = AnalysisService()
    if not GEMINI_API_KEY:
        raise ValueError("GEMINI_API_KEY environment variable not set!")
    # Setup MongoDB connection
    client = MongoClient("mongodb://localhost:27017")
    db = client["MentalHealth"]
    users_collection = db["users"]
    chat_collection = db["chats"]
    # Initialize the main chatbot service
    chatbot_service = ChatbotService(
        users_collection=users_collection,
        chat_collection=chat_collection,
        analysis_service=analysis_service
    )
    print(" Chatbot Service is ready to accept requests.")

except Exception as e:
    print(f" CRITICAL ERROR during initialization: {e}")
    chatbot_service = None
# --- API Routes ---
@app.route("/api/chat", methods=["POST"])
def chat():
    if not chatbot_service:
        return jsonify({"error": "Chatbot service is not available due to an initialization error."}), 503
    data = request.get_json()
    u_id = data.get("user_id")
    message = data.get("message")

     db_manager = DatabaseManager(users_collection,chat_collection)
    user = db_manager.get_user_by_id(u_id)
    return jsonify(user) 

    if not u_id or not message:
        return jsonify({"error": "user_id and message are required."}), 400
    try:
        response_payload = chatbot_service.handle_chat_request(u_id, message)
        return jsonify(response_payload)
    except Exception as e:
        print(f"An error occurred during chat handling: {e}")
        return jsonify({"error": "An internal error occurred."}), 500

if __name__ == "__main__":
    app.run(debug=True,use_reloader=False) """