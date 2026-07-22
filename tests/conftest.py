import pytest

from app import create_app
from app.extensions import db as _db

FAKE_COINS = [{
    "id": "bitcoin",
    "symbol": "btc",
    "name": "Bitcoin",
    "image": "",
    "current_price": 100.0,
    "market_cap_rank": 1,
    "price_change_percentage_24h": 0,
}]


@pytest.fixture
def app():
    """Instance Flask isolée pour les tests, avec une base SQLite en mémoire."""
    application = create_app({
        "TESTING": True,
        "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:",
    })

    yield application

    with application.app_context():
        _db.session.remove()
        _db.drop_all()


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture(autouse=True)
def no_external_calls(monkeypatch):
    """Empêche les tests de faire de vrais appels réseau (CoinGecko, flux RSS)."""

    def fake_get_market_data(*args, **kwargs):
        return FAKE_COINS

    def fake_get_coin(coin_id, *args, **kwargs):
        for coin in FAKE_COINS:
            if coin["id"] == coin_id:
                return coin
        return None

    def fake_get_articles(*args, **kwargs):
        return []

    monkeypatch.setattr("app.market.coingecko.get_market_data", fake_get_market_data)
    monkeypatch.setattr("app.trading.routes.get_market_data", fake_get_market_data)
    monkeypatch.setattr("app.trading.routes.get_coin", fake_get_coin)
    monkeypatch.setattr("app.news.rss.get_latest_articles", fake_get_articles)


def register(client, username="alice", email="alice@test.local", password="Test1234!"):
    return client.post("/auth/register", data={
        "username": username,
        "email": email,
        "password": password,
    }, follow_redirects=True)


def login(client, email="alice@test.local", password="Test1234!"):
    return client.post("/auth/login", data={
        "email": email,
        "password": password,
    }, follow_redirects=True)
