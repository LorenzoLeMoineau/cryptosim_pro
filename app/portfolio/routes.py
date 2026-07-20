from flask import render_template
from flask_login import login_required, current_user

from app.portfolio import bp
from app.market.coingecko import get_coin_price


@bp.route("/portfolio")
@login_required
def index():
    holdings_data = []
    total_holdings_value = 0.0
    total_invested = 0.0

    for holding in current_user.holdings:
        if holding.quantity <= 0:
            continue

        current_price = get_coin_price(holding.coin_id) or 0.0
        current_value = holding.quantity * current_price
        cost_basis = holding.quantity * holding.avg_buy_price
        profit_loss = current_value - cost_basis
        profit_loss_pct = (profit_loss / cost_basis * 100) if cost_basis > 0 else 0.0

        total_holdings_value += current_value
        total_invested += cost_basis

        holdings_data.append({
            "coin_id": holding.coin_id,
            "quantity": holding.quantity,
            "avg_buy_price": holding.avg_buy_price,
            "current_price": current_price,
            "current_value": current_value,
            "profit_loss": profit_loss,
            "profit_loss_pct": profit_loss_pct,
        })

    for h in holdings_data:
        h["allocation_pct"] = (
            (h["current_value"] / total_holdings_value * 100) if total_holdings_value > 0 else 0.0
        )

    holdings_data.sort(key=lambda h: h["current_value"], reverse=True)

    total_profit_loss = total_holdings_value - total_invested
    total_profit_loss_pct = (
        (total_profit_loss / total_invested * 100) if total_invested > 0 else 0.0
    )
    portfolio_value = current_user.cash_balance + total_holdings_value

    return render_template(
        "portfolio.html",
        holdings_data=holdings_data,
        total_holdings_value=total_holdings_value,
        total_profit_loss=total_profit_loss,
        total_profit_loss_pct=total_profit_loss_pct,
        portfolio_value=portfolio_value,
    )
