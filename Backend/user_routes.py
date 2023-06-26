from flask import Blueprint, request, session, jsonify
import user_utils

# pylint: disable=fixme
# TODO - understand the error codes in the API (400, 500, etc.)

# create a blueprint for the user routes

user_routes = Blueprint("user_routes", __name__)


@user_routes.route("/register", methods=["POST"])
def register():
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")
    email = data.get("email")

    if not username or not password or not email:
        return jsonify({"error": "Invalid data"}), 400

    user = user_utils.create_user(username, email, password)
    if not user:
        return jsonify({"error": "User could not be created"}), 500

    return jsonify({"success": "User registered successfully"}), 200


@user_routes.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")

    if not username or not password:
        return jsonify({"error": "Missing username or password"}), 400
    if user_utils.find_user(username=username) is None:
        return jsonify({"error": "User not found"}), 404

    user = user_utils.find_user(username=username)
    if user is None or not user.check_password(password):
        return jsonify({"error": "Invalid username or password"}), 401

    session["user_id"] = user.id
    return jsonify({"success": "Logged in successfully"}), 200


@user_routes.route("/delete_user", methods=["DELETE"])
def delete_user():
    data = request.get_json()
    username = data.get("username")
    email = data.get("email")

    if not username and not email:
        return jsonify({"error": "Missing username or email"}), 400

    user_utils.delete_user(username=username, email=email)

    return jsonify({"success": "User deleted successfully"}), 200
