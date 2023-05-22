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
    if not username or not email or not password:
        print("You need to provide a username, an email and a password.")
        return
    with app.app_context():
        # Check if user already exists
        existing_user = User.query.filter_by(username=username).first()
        if existing_user is not None:
            print(f"User with username {username} already exists.")
            return

        # Create new user
        user = User(username=username, email=email)
        user.set_password(password)

        # Add new user to database
        db.session.add(user)
        db.session.commit()

        print(f"User {username} created successfully.")
        return user


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
                return

        # If only one of them is provided, query user by that
        elif email:
            user = User.query.filter_by(email=email).first()
        elif username:
            user = User.query.filter_by(username=username).first()
        else:
            print("You need to provide either an email or a username.")
            return

        return user


def delete_user(username=None, email=None):
    with app.app_context():
        # Query user by email or username
        if username and email:
            user = find_user(username=username, email=email)
            if user is None:
                print("User not found.")
                return
        elif username:
            user = find_user(username=username)
        elif email:
            user = find_user(email=email)
        else:
            print("You need to provide either an email or a username.")
            return

        # Delete user
        db.session.delete(user)
        db.session.commit()
