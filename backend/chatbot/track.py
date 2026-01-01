from flask import request, jsonify, current_app
from datetime import datetime
from bson import ObjectId


# Emotion text mapping
emotionstxt = {
    0:"admiration",1:"amusement",2:"anger",3:"annoyance",4:"approval",
    5:"caring",6:"confusion",7:"curiosity",8:"desire",9:"disappointment",
    10:"disapproval",11:"disgust",12:"embarrassment",13:"excitement",14:"fear",
    15:"gratitude",16:"grief",17:"joy",18:"love",19:"nervousness",20:"optimism",
    21:"pride",22:"realization",23:"relief",24:"remorse",25:"sadness",
    26:"surprise",27:"neutral"
}

# Custom emotion scores (0 = most negative, 1 = most positive)
emotion_scores = {
    "anger": 0.1, "annoyance": 0.2, "disappointment": 0.2, "disapproval": 0.2,
    "disgust": 0.1, "fear": 0.1, "grief": 0.0, "remorse": 0.1, "sadness": 0.0,
    "nervousness": 0.3, "confusion": 0.3, "neutral": 0.5, "curiosity": 0.6,
    "desire": 0.6, "realization": 0.7, "admiration": 0.8, "approval": 0.8,
    "caring": 0.8, "gratitude": 0.9, "joy": 1.0, "love": 1.0, "optimism": 0.9,
    "pride": 0.9, "amusement": 0.9, "excitement": 1.0, "surprise": 0.7,
    "embarrassment": 0.2
}

def get_emotion_history():
    data = request.get_json()
    user_id = data.get("user_id")
    #user_id = request.args.get("user_id")
    if not user_id:
        return jsonify({"error": "user_id is required"}), 400

    users = current_app.config["CHATS_COLLECTION"]
    user_doc = users.find_one({"userId": ObjectId(user_id)})

    if not user_doc:
        return jsonify({"error": "User not found"}), 404

    mood_history = []
    for item in user_doc.get("moodHistory", []):
        date = item.get("timestamp", datetime.utcnow())
        emotion_raw = item.get("emotion", "neutral")
        if isinstance(emotion_raw, str):
            mood_name = emotion_raw
        else:
            mood_name = emotionstxt.get(emotion_raw.get("category", 0), "neutral")
        score = emotion_scores.get(mood_name, 0.5)
        mood_history.append({
            "timestamp": date,
            "emotion": mood_name,
            "emotion_score": score
        })
    return jsonify(mood_history)

def get_chat_history():
    data = request.get_json()
    user_id = data.get("user_id")
    print("oooooo")
    if not user_id:
        return jsonify({"error": "user_id is required"}), 400

    users = current_app.config["CHATS_COLLECTION"]
    user_doc = users.find_one({"userId": ObjectId(user_id)})

    if not user_doc:
        return jsonify({"error": "User not found"}), 404

    chatHistory = []
    for item in user_doc.get("conversations", []):
        raw_date = item.get("timestamp", datetime.utcnow())
        if isinstance(raw_date, dict) and "$date" in raw_date:
            date = raw_date["$date"]
        else:
            date = raw_date
        user_query = item.get("user")
        bot_resp = item.get("bot")
        chatHistory.append({
            "timestamp": date,
            "message": user_query,
            "response": bot_resp
        })
    chatHistory.sort(key=lambda x: x["timestamp"])
    return jsonify({ "chats": [{ "chatHistory": chatHistory }] })

