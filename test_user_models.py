import user_models
from app import app

# pylint: disable=fixme
# TODO change db to test database


def test_models_password():
    user = user_models.User()
    user.set_password("password")
    assert user.check_password("password") is True
    assert user.check_password("not password") is False


def test_add_user():
    with app.app_context():
        user_models.db.create_all()

        user = user_models.User()
        user.username = "test_user"
        user.email = "test@testing.com"
        user.set_password("password")
        user_models.db.session.add(user)
        user_models.db.session.commit()
        assert (
            user_models.User.query.filter_by(username="test_user").first() is not None
        )
        assert (
            user_models.User.query.filter_by(username="test_user")
            .first()
            .check_password("password")
            is True
        )
        assert (
            user_models.User.query.filter_by(username="test_user")
            .first()
            .check_password("not password")
            is False
        )
        user_models.db.session.delete(user)
        user_models.db.session.commit()
        assert user_models.User.query.filter_by(username="test_user").first() is None
