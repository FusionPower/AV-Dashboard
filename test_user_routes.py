import os
import tempfile
import pytest

from flask import json
from app import app
from extensions import db


# pylint: disable=redefined-outer-name
# pylint: disable=fixme
# TODO make success mesages more robust


@pytest.fixture
def test_client():
    db_file_descriptor, app.config["DATABASE"] = tempfile.mkstemp()
    app.config["TESTING"] = True

    with app.test_client() as client:
        with app.app_context():
            db.create_all()
        yield client

    os.close(db_file_descriptor)
    os.unlink(app.config["DATABASE"])


def test_register_and_login(test_client):
    # Register
    response = test_client.post(
        "/register",
        data=json.dumps(
            {
                "username": "test_user",
                "email": "test@test.com",
                "password": "password",
            }
        ),
        content_type="application/json",
    )

    # data = json.loads(response.data)
    assert response.status_code == 200
    assert b"successfully" in response.data
    # assert data['status'] == 'success'
    # assert data['message'] == 'User registered successfully'

    # Login
    response = test_client.post(
        "/login",
        data=json.dumps(
            {
                "username": "test_user",
                "password": "password",
            }
        ),
        content_type="application/json",
    )

    assert response.status_code == 200
    assert b" successfully" in response.data

    # Delete
    response = test_client.delete(
        "/delete_user",
        data=json.dumps(
            {
                "username": "test_user",
                "email": "test@test.com",
            }
        ),
        content_type="application/json",
    )
    assert response.status_code == 200

