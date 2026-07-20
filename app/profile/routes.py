from flask import render_template
from flask_login import login_required, current_user

from app.profile import bp
from app.models import Transaction
from app.market.coingecko import get_coin_price

STARTING_BALANCE = 10000.0  # doit rester synchro avec User.cash_balance (app/models.py)


@bp.route("/profile")
@login_required
def index():
    total_trades = Transaction.query.filter_by(user_id=current_user.id).count()
    buy_count = Transaction.query.filter_by(user_id=current_user.id, type="buy").count()
    sell_count = Transaction.query.filter_by(user_id=current_user.id, type="sell").count()

    holdings_value = sum(
        holding.quantity * (get_coin_price(holding.coin_id) or 0.0)
        for holding in current_user.holdings
    )
    portfolio_value = current_user.cash_balance + holdings_value
    performance_pct = (portfolio_value - STARTING_BALANCE) / STARTING_BALANCE * 100

    return render_template(
        "profile.html",
        total_trades=total_trades,
        buy_count=buy_count,
        sell_count=sell_count,
        starting_balance=STARTING_BALANCE,
        portfolio_value=portfolio_value,
        performance_pct=performance_pct,
    )
