from flask import request, jsonify ,current_app
from bson import ObjectId
from datetime import datetime, timedelta
import jwt
from auth_helper import hash_password,compare_password
from models import create_user,find_by_email,update_password


def register_controller():
    print("this is runnnnnnnnnnnnnnnn222222222222222222")

    users = current_app.config["USERS_COLLECTION"]
    data = request.get_json()

    name, email, password, answer, gender = (
        data.get("name"),
        data.get("email"),
        data.get("password"),
        data.get("answer"),
        data.get("selectedGender")
    )
    #"age":"ages"

    if not all([name, email, password, answer]):
        return jsonify({"success": False, "message": "Missing required fields"}), 400

    existing_user = find_by_email(users, email)
    if existing_user:
        return jsonify({"success": False, "message": "Already registered, please login"}), 400

    hashed = hash_password(password)

    user = {
        "name": name,
        "email": email,
        "password": hashed,
        "answer": answer,
        "gender":gender,
    }
    user_id=create_user(users,user)
    user["_id"] = str(user_id)
    del user["password"]
    return jsonify({"success": True, "message": "User registered successfully", "user": user}), 201

# Login Controller
def login_controller():
    users = current_app.config["USERS_COLLECTION"]
    data = request.get_json()

    email, password = (data.get("email"),data.get("password"))
    JWT_SECRET = current_app.config["JWT_SECRET"]
    if not email or not password:
        return jsonify({"success": False, "message": "Invalid email or password"}), 400

    user = find_by_email(users, email)
    if not user:
        return jsonify({"success": False, "message": "Email is not registered"}), 404

    if not compare_password(password, user['password']):
        return jsonify({"success": False, "message": "Invalid password"}), 401
    token = jwt.encode(
        {"_id": str(user["_id"]), "exp": datetime.utcnow() + timedelta(days=7)},
        JWT_SECRET,
        algorithm="HS256"
    )
    return jsonify({
        "success": True,
        "message": "Login successfully",
        "user": {
            "_id": str(user["_id"]),
            "name": user["name"],
            "email": user["email"]
        },
        "token": token
    }), 200

# Forgot Password Controller
def forgot_password_controller():
    users = current_app.config["USERS_COLLECTION"]
    data = request.get_json()

    email,answer,new_password =(
        data.get('email'),
        data.get('answer'),
        data.get('newPassword')
    )

    if not all([ email, answer,new_password]):
        return jsonify({"success": False, "message": "Missing required fields"}), 400

    user = users.find_one({"email": email, "answer": answer})
    if not user:
        return jsonify({"success": False, "message": "Wrong email or answer"}), 404

    hashed = hash_password(new_password)
    update_password(users,user["_id"],hashed)
    return jsonify({"success": True, "message": "Password reset successfully"}), 200


# Test Controller (Protected Route)
def test_controller():
    try:
        return jsonify("Protected Route Accessed")
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    


