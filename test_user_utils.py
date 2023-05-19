import user_utils
from user_routes import app
from user_models import db

# fmt: off


def test_user_utils():
    with app.app_context():
        # Change db to test database
        db.drop_all()
        db.create_all()

        # Check if get_all_users returns at least 1 user
        user_utils.create_user("test_user", "test@test.com", "password")
        assert (len(user_utils.get_all_users()) >= 1), "get_all_users() should return at least 1 user"

        # Check if the test user is in the database
        assert (user_utils.find_user(username="test_user")) is not None, "find_user() by username should return the test user"
        assert (user_utils.find_user(email="test@test.com")) is not None, "find_user() by email should return the test user"
        assert (user_utils.find_user(username="test_user", email="test@test.com")) is not None, "find_user() by email and username should return the test user"

        # Check if the test user is not in the database
        assert (user_utils.find_user(username="not_test_user")) is None, "find_user() by username should not return the test user"
        assert (user_utils.find_user(email="not_test_user@test.com")) is None, "find_user() by email should not return the test user"
        assert (user_utils.find_user(username="not_test_user", email="test@test.com")) is None, "find_user() by email and wrong username should return None"
        assert (user_utils.find_user(username="test_user", email="not_test_user@test.com")) is None, "find_user() by wrong email and username should return None"

        # Check null inputs
        assert (user_utils.find_user()) is None, "find_user() with no arguments should return None"
        assert (user_utils.delete_user()) is None, "delete_user() with no arguments should return None"

        # Delete the test user
        user_utils.delete_user(username="test_user")
        assert (user_utils.find_user(username="test_user")) is None, "find_user() by username should not return the test user after deletion"
