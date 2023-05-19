import models
from user_routes import app

# pylint: disable=fixme
# TODO change db to test database


def test_models_password():
    user = models.User()
    user.set_password("password")
    assert user.check_password("password") is True
    assert user.check_password("not password") is False


def test_add_user():
    with app.app_context():
        models.db.create_all()

        user = models.User()
        user.username = "test_user"
        user.email = "test@testing.com"
        user.set_password("password")
        models.db.session.add(user)
        models.db.session.commit()
        assert models.User.query.filter_by(username="test_user").first() is not None
        assert (
            models.User.query.filter_by(username="test_user")
            .first()
            .check_password("password")
            is True
        )
        assert (
            models.User.query.filter_by(username="test_user")
            .first()
            .check_password("not password")
            is False
        )
        models.db.session.delete(user)
        models.db.session.commit()
        assert models.User.query.filter_by(username="test_user").first() is None
