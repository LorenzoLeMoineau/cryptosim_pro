from app.extensions import db
from app.market.coingecko import get_coin_price


def check_price_alerts(user):
    """Vérifie les alertes actives de l'utilisateur et marque celles déclenchées."""
    triggered_now = []

    for alert in user.price_alerts:
        if alert.triggered:
            continue

        current_price = get_coin_price(alert.coin_id)
        if current_price is None:
            continue

        if alert.direction == "above" and current_price >= alert.target_price:
            alert.triggered = True
            triggered_now.append(alert)
        elif alert.direction == "below" and current_price <= alert.target_price:
            alert.triggered = True
            triggered_now.append(alert)

    if triggered_now:
        db.session.commit()

    return triggered_now
