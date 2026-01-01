from functools import wraps
from flask import request, jsonify,g
import jwt
from pymongo import MongoClient
import os
from dotenv import load_dotenv

load_dotenv()

# Middleware: Token Required
def require_signin(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        print("some wrong888888888")
        token = request.headers.get("Authorization")
        print(token)
        JWT_SECRET = os.getenv("JWT_SECRET")
        if not token:
            return jsonify({"message": "Token is missing!"}), 401

        try:
            decoded = jwt.decode(token, JWT_SECRET, algorithms=["HS256"])
            g.user = decoded  # Store user info in request
        except jwt.ExpiredSignatureError:
            return jsonify({"message": "Token expired"}), 401
        except jwt.InvalidTokenError:
            return jsonify({"message": "Invalid token"}), 401
        except Exception as e:
            return jsonify({"message": "Auth error", "error": str(e)}), 401

        return f(*args, **kwargs)

    return decorated_function
