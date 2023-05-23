from user_models import User
from extensions import db
from flask import current_app as app

# pylint: disable=fixme,no-member

# TODO - Implement the following functions:
# alter_user


def get_all_users():
    with app.app_context():
        # Query all users
        users = User.query.all()

        return users


def create_user(username, email, password):
    # TODO check username, email and password validity
    with app.app_context():
        if not username or not email or not password:
            return None, "Must provide username, email and password"

        # Check if user already exists
        existing_user = User.query.filter_by(username=username).first()
        if existing_user is not None:
            return None, f"User with username {username} already exists."

        # Create new user
        user = User(username=username, email=email)
        user.set_password(password)
        if not user:
            return None, "User could not be created."
        # Add new user to database
        db.session.add(user)
        db.session.commit()
        db.session.refresh(user)

        return user, "User Created"


def find_user(username=None, email=None):
    with app.app_context():
        # If both username and email are provided, check if they match
        if email and username:
            email_user = User.query.filter_by(email=email).first()
            username_user = User.query.filter_by(username=username).first()
            if email_user == username_user:
                user = email_user
            else:
                print("Email and username do not match.")
                return None

        # If only one of them is provided, query user by that
        elif email:
            user = User.query.filter_by(email=email).first()
        elif username:
            user = User.query.filter_by(username=username).first()
        else:
            print("You need to provide either an email or a username.")
            return None

        return user


def delete_user(username=None, email=None):
    with app.app_context():
        # Query user by email or username
        if not username and not email:
            raise ValueError("Must provide either username or id")

        if username and email:
            user = find_user(username=username, email=email)
            if user is None:
                return "User not found."
        elif username:
            user = find_user(username=username)
        elif email:
            user = find_user(email=email)
        else:
            return "You need to provide either an email or a username."

        # Delete user
        db.session.delete(user)
        db.session.commit()
        return "User Deleted"


def login(username=None, password=None):
    with app.app_context():
        if not username or not password:
            return None
        user = find_user(username=username)
        if user is None:
            return None
        if user.check_password(password):
            return user
        else:
            return None
