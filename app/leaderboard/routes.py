from flask import render_template
from flask_login import login_required, current_user

from app.leaderboard import bp
from app.models import User
from app.market.coingecko import get_coin_price

STARTING_BALANCE = 10000.0  # doit rester synchro avec User.cash_balance (app/models.py)


@bp.route("/leaderboard")
@login_required
def index():
    rankings = []

    for user in User.query.all():
        holdings_value = sum(
            holding.quantity * (get_coin_price(holding.coin_id) or 0.0)
            for holding in user.holdings
        )
        portfolio_value = user.cash_balance + holdings_value
        performance_pct = (portfolio_value - STARTING_BALANCE) / STARTING_BALANCE * 100

        rankings.append({
            "user_id": user.id,
            "username": user.username,
            "portfolio_value": portfolio_value,
            "performance_pct": performance_pct,
        })

    rankings.sort(key=lambda r: r["portfolio_value"], reverse=True)
    top_rankings = rankings[:10]

    for i, entry in enumerate(top_rankings, start=1):
        entry["rank"] = i

    current_user_rank = next(
        (i for i, r in enumerate(rankings, start=1) if r["user_id"] == current_user.id),
        None,
    )

    return render_template(
        "leaderboard.html",
        rankings=top_rankings,
        current_user_rank=current_user_rank,
        total_users=len(rankings),
    )
