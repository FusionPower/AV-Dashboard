import user_model
from flask import Flask
from main import db, app



def test_user_model_password():
    user = user_model.User()
    user.set_password('password')
    assert user.check_password('password') is True
    assert user.check_password('not password') is False


def test_add_user():
    with app.app_context():
        db.create_all()

        user = user_model.User()
        user.username = 'test_user'
        user.email = 'test@testing.com'
        user.set_password('password')
        user_model.db.session.add(user)
        user_model.db.session.commit()
        assert user_model.User.query.filter_by(username='test_user').first() is not None
        assert user_model.User.query.filter_by(username='test_user').first().check_password('password') is True
        assert user_model.User.query.filter_by(username='test_user').first().check_password('not password') is False
        user_model.db.session.delete(user)
        user_model.db.session.commit()
        assert user_model.User.query.filter_by(username='test_user').first() is None

