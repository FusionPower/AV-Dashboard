from graphene.test import Client
from user_models import User
from schema import schema
from extensions import db
from app import app
import tempfile
import os
from simulation_models import SimulationType

# pylint: disable=fixme,no-member


def add_test_user():
    new_user = User(username="testuser", email="testuser@email.com")
    new_user.set_password("testpassword")
    db.session.add(new_user)
    db.session.commit()

def add_test_simulation_type():
    new_simulation_type = SimulationType(name="Test Simulation", description="testdescription")
    db.session.add(new_simulation_type)
    db.session.commit()

def config_test():
    db_fd, app.config["DATABASE"] = tempfile.mkstemp()
    app.config["TESTING"] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + app.config["DATABASE"]
    db.create_all()
    return db_fd

def end_test(db_fd):
    db.drop_all()
    os.close(db_fd)
    os.unlink(app.config["DATABASE"])

def test_create_user():
    # Set up Flask testing environment
    app.config["TESTING"] = True
    with app.app_context():
        db_fd = config_test()
        client = Client(schema)
        executed = client.execute(
            """
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
        """
        )

        assert executed == {
            "data": {
                "createUser": {
                    "ok": "User Created",
                    "user": {
                        "id": "1",
                        "username": "testuser",
                        "email": "testuser@email.com",
                    },
                }
            }
        }
        end_test(db_fd)


def test_query_user():
    app.config["TESTING"] = True

    with app.app_context():
        db_fd = config_test()
        add_test_user()
        client = Client(schema)

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
        assert executed == {
            "data": {
                "user": {
                    "id": "1",
                    "username": "testuser",
                    "email": "testuser@email.com",
                }
            }
        }
        end_test(db_fd)


def test_delete_user():
    app.config["TESTING"] = True
    with app.app_context():
        db_fd = config_test()
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
        assert executed == {"data": {"deleteUser": {"ok": "User Deleted"}}}

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
        assert executed == {"data": {"deleteUser": {"ok": "User Deleted"}}}

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
        assert executed == {"data": {"deleteUser": {"ok": "User Deleted"}}}
        end_test(db_fd)



def test_create_simulation_type():
    app.config["TESTING"] = True
    with app.app_context():
        db_fd = config_test()
        client = Client(schema)

        executed = client.execute(
            """
            mutation {
                createSimulationType(name: "Test Simulation", description: "testdescription") {
                    ok
                    simulationType {
                        id
                        name
                        description
                    }
                }
            }
            """
        )

        assert executed == {
            "data": {
                "createSimulationType": {
                "ok": "Simulation Type Created",
                "simulationType": {
                    "id": "1",
                    "name": "Test Simulation",
                    "description": "testdescription"
                }
                }
            }
        }
        end_test(db_fd)

def test_query_simulation_type():
    app.config["TESTING"] = True
    with app.app_context():
        db_fd = config_test()
        client = Client(schema)

        add_test_simulation_type()
        executed = client.execute(
            """
            query {
                simulationType(id: "1") {
                    id
                    name
                    description
                }
            }
            """
        )

        assert executed == {
            "data": {
                "simulationType": {
                    "id": "1",
                    "name": "Test Simulation",
                    "description": "testdescription"
                }
            }
        }
        end_test(db_fd)

# def test_update_simulation_type():
#     app.config["TESTING"] = True
#     with app.app_context():
#         db_fd = config_test()
#         client = Client(schema)

#         add_test_simulation_type()
#         executed = client.execute(
#             """
#             mutation {
#                 updateSimulationType(id: "1", name: "Updated Simulation", description: "updateddescription") {
#                     ok
#                     simulationType {
#                         id
#                         name
#                         description
#                     }
#                 }
#             }
#             """
#         )

#         assert executed == {
#             "data": {
#                 "updateSimulationType": {
#                     "ok": "Simulation Type Updated",
#                     "simulationType": {
#                         "id": "1",
#                         "name": "Updated Simulation",
#                         "description": "updateddescription"
#                     }
#                 }
#             }
#         }
#         end_test(db_fd)
