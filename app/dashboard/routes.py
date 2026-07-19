from flask import render_template
from flask_login import login_required, current_user

from app.dashboard import bp
from app.market.coingecko import get_coin_price
from app.models import Transaction


@bp.route("/dashboard")
@login_required
def index():
    holdings_value = 0.0
    invested_value = 0.0
    holdings_data = []

    for holding in current_user.holdings:
        if holding.quantity <= 0:
            continue

        current_price = get_coin_price(holding.coin_id) or 0.0
        current_value = holding.quantity * current_price
        cost_basis = holding.quantity * holding.avg_buy_price

        holdings_value += current_value
        invested_value += cost_basis

        holdings_data.append({
            "coin_id": holding.coin_id,
            "quantity": holding.quantity,
            "current_price": current_price,
            "current_value": current_value,
            "profit_loss": current_value - cost_basis,
        })

    portfolio_value = current_user.cash_balance + holdings_value
    total_gain_loss = holdings_value - invested_value

    recent_transactions = (
        Transaction.query.filter_by(user_id=current_user.id)
        .order_by(Transaction.timestamp.desc())
        .limit(5)
        .all()
    )

    return render_template(
        "dashboard.html",
        cash_balance=current_user.cash_balance,
        portfolio_value=portfolio_value,
        total_gain_loss=total_gain_loss,
        holdings_data=holdings_data,
        recent_transactions=recent_transactions,
    )
