from flask import Blueprint,jsonify

from controllers.auth_controller import register_controller, login_controller, forgot_password_controller, test_controller
from auth_middleware import require_signin

auth_bp = Blueprint('auth_bp', __name__, url_prefix='/api/v1/auth')

@auth_bp.route("/register", methods=["POST"])
def register():
    print("Register route hit")
    return register_controller()

@auth_bp.route("/login", methods=["POST"])
def login():
    return login_controller()

@auth_bp.route("/forgot-password", methods=["POST"])
def forgot_password():
    return forgot_password_controller()

@auth_bp.route("/user-auth", methods=["GET"])
@require_signin
def user_auth():
    print("here we are")
    return jsonify({"ok": True}), 200

@auth_bp.route("/test", methods=["GET"])
@require_signin
def test():
    return test_controller()

