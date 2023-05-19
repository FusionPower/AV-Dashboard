from flask import Flask, request, session, jsonify
from user_models import User
from database import db, bcrypt
import user_utils

# pylint: disable=fixme
# TODO - understand the error codes in the API (400, 500, etc.)

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:////tmp/test.db"
app.config["SECRET_KEY"] = "sample_dummy_secret_key"
db.init_app(app)
bcrypt.init_app(app)


# @app.route("/delete_user", methods=["POST"])
# def delete_user():
#     data = request.get_json()
#     username = data.get("username")
#     email = data.get("email")

#     if not username and not email:
#         return jsonify({"error": "Missing username or email"}), 400

#     user_utils.delete_user(username=username, email=email)


@app.route("/register", methods=["POST"])
def register():
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")
    email = data.get("email")

    if not username or not password or not email:
        return jsonify({"error": "Invalid data"}), 400

    user_utils.create_user(username, email, password)
    user = user_utils.find_user(username=username, email=email)
    if not user:
        return jsonify({"error": "User could not be created"}), 500

    return jsonify({"success": "User registered successfully"}), 200


@app.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")

    if not username or not password:
        return jsonify({"error": "Missing username or password"}), 400
    if user_utils.find_user(username=username) is None:
        return jsonify({"error": "User not found"}), 404

    user = User.query.filter_by(username=username).first()
    if user is None or not user.check_password(password):
        return jsonify({"error": "Invalid username or password"}), 401

    session["user_id"] = user.id
    return jsonify({"success": "Logged in successfully"}), 200


if __name__ == "__main__":
    app.run(debug=True)
