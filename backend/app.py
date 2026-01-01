from flask import Flask, request
from flask_cors import CORS
import os
from dotenv import load_dotenv
from pymongo import MongoClient
from routes.auth_routes import auth_bp
from routes.chatbot_routes import chatbot_bp
load_dotenv()

app = Flask(__name__)
CORS(app)

client = MongoClient("mongodb://localhost:27017/")
db = client["MentalHealth"]

# Config
app.config["JWT_SECRET"] = os.getenv("JWT_SECRET")
app.config["USERS_COLLECTION"] = db["users"]
app.config["CHATS_COLLECTION"] = db["chats"]

app.register_blueprint(auth_bp)
app.register_blueprint(chatbot_bp)

@app.before_request
def log_request():
    if request.is_json:
        print(f"{request.method} {request.path} - {request.get_json()}")

@app.route("/")
def home():
    return "<h1>Welcome to Mental Health </h1>"

""" if __name__ == "__main__":
    print("Starting Flask App...")
    app.run(host="0.0.0.0",port=5000,debug=False)  """
