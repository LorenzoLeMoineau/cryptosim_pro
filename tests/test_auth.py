from app.models import User

from conftest import register, login


def test_register_success(client, app):
    response = register(client)
    assert response.status_code == 200

    with app.app_context():
        user = User.query.filter_by(username="alice").first()
        assert user is not None
        assert user.email == "alice@test.local"
        assert user.password_hash != "Test1234!"  # jamais stocké en clair


def test_register_duplicate_username(client):
    register(client, username="alice", email="alice1@test.local")
    response = register(client, username="alice", email="alice2@test.local")

    page = response.get_data(as_text=True)
    assert "déjà pris" in page


def test_login_wrong_password(client):
    register(client)
    response = login(client, password="WrongPassword!")

    page = response.get_data(as_text=True)
    assert "incorrect" in page
