import pytest
from graphene.test import Client
from user_models import User
from schema import schema
from extensions import db
from app import app


# TODO make dummy database for testing


def add_test_user():
    # Add test user
    new_user = User(username="testuser", email="testuser@email.com")
    new_user.set_password("testpassword")
    db.session.add(new_user)
    db.session.commit()


def test_create_user():
    # Set up Flask testing environment
    app.config["TESTING"] = True
    with app.app_context():
        # Initialize database
        db.drop_all()
        db.create_all()

        # Set up Graphene test client
        client = Client(schema)

        # Run createUser mutation
        executed = client.execute("""
        mutation {
            createUser(username: "testuser", email: "testuser@email.com", password: "testpassword") {
                ok
                user {
                    id
                    username
                    email
                }
            }
        }
        """)

        # Check result
        assert executed == {
            "data": {
                "createUser": {
                    "ok": "User Created",
                    "user": {
                        "id": "1",
                        "username": "testuser",
                        "email": "testuser@email.com"
                    }
                }
            }
        }

def test_query_user():
    # Set up Flask testing environment
    app.config["TESTING"] = True

    with app.app_context():
        # Initialize database
        db.drop_all()
        db.create_all()

        add_test_user()

        # Set up Graphene test client
        client = Client(schema)

        # Run user query
        executed = client.execute(
        """
            query {
                user(id: "1") {
                    id
                    username
                    email
                }
            }
        """
        )

        # Check result
        assert executed == {
            "data": {
                "user": {
                    "id": "1",
                    "username": "testuser",
                    "email": "testuser@email.com"
                }
            }
        }

def test_delete_user():
    app.config["TESTING"] = True

    with app.app_context():
        db.drop_all()
        db.create_all()
        client = Client(schema)

        # Test delete by username
        add_test_user()
        executed = client.execute(
            """
            mutation {
                deleteUser(username: "testuser") {
                    ok
                }
            }
            """
        )
        assert executed == {
            "data": {
                "deleteUser": {
                "ok": "User Deleted"
                }
            } 
        }

        # Test delete by email
        add_test_user()
        executed = client.execute(
            """
            mutation {
                deleteUser(email: "testuser@email.com") {
                    ok
                }
            }
            """
        )
        assert executed == {
            "data": {
                "deleteUser": {
                "ok": "User Deleted"
                }
            } 
        }

        # Test delete by username and email
        add_test_user()
        executed = client.execute(
            """
            mutation {
                deleteUser(username: "testuser", email: "testuser@email.com") {
                    ok
                }
            }
            """
        )
        assert executed == {
            "data": {
                "deleteUser": {
                "ok": "User Deleted"
                }
            } 
        }



