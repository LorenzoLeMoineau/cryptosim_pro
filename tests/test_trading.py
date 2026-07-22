from app.models import User

from conftest import register, login


def test_buy_success(client, app):
    register(client)
    login(client)

    response = client.post("/trading", data={
        "action": "buy",
        "coin_id": "bitcoin",
        "quantity": "1",
    }, follow_redirects=True)

    assert response.status_code == 200

    with app.app_context():
        user = User.query.filter_by(username="alice").first()
        # prix 100 + frais 0.5% (0.5) = 100.5 débités des 10 000 de départ
        assert user.cash_balance == 9899.5
        assert len(user.holdings) == 1
        assert user.holdings[0].coin_id == "bitcoin"
        assert user.holdings[0].quantity == 1.0


def test_buy_insufficient_balance(client, app):
    register(client)
    login(client)

    client.post("/trading", data={
        "action": "buy",
        "coin_id": "bitcoin",
        "quantity": "1000",  # coûterait 100 000$, largement plus que le solde de départ
    }, follow_redirects=True)

    with app.app_context():
        user = User.query.filter_by(username="alice").first()
        assert user.cash_balance == 10000.0
        assert len(user.holdings) == 0


def test_sell_insufficient_quantity(client, app):
    register(client)
    login(client)

    client.post("/trading", data={
        "action": "sell",
        "coin_id": "bitcoin",
        "quantity": "1",
    }, follow_redirects=True)

    with app.app_context():
        user = User.query.filter_by(username="alice").first()
        assert user.cash_balance == 10000.0
        assert len(user.holdings) == 0
