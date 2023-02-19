from api.models import users as user_model


def test_user_model_repr():
    user = user_model.User(id=1, name="hoge", password="9akldsjf9")
    assert str(user) == f"<User ({user.id}, {user.name})>"
