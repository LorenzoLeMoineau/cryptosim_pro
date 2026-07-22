from flask import render_template, request, redirect, url_for, flash, jsonify
from flask_login import login_required, current_user

from app.trading import bp
from app.extensions import db
from app.models import Holding, Transaction
from app.market.coingecko import get_market_data, get_coin

FEE_RATE = 0.005


@bp.route("/trading/price/<coin_id>")
@login_required
def price(coin_id):
    coin = get_coin(coin_id)
    if coin is None:
        return jsonify({"error": "not_found"}), 404
    return jsonify({"price": coin["current_price"]})


@bp.route("/trading", methods=["GET", "POST"])
@login_required
def index():
    coins = get_market_data()

    if request.method == "POST":
        action = request.form.get("action")
        coin_id = request.form.get("coin_id")
        quantity_raw = request.form.get("quantity", "")

        try:
            quantity = float(quantity_raw)
        except ValueError:
            flash("Quantité invalide.", "error")
            return redirect(url_for("trading.index", coin=coin_id))

        if quantity <= 0:
            flash("La quantité doit être supérieure à 0.", "error")
            return redirect(url_for("trading.index", coin=coin_id))

        coin = get_coin(coin_id)
        if coin is None:
            flash("Cryptomonnaie introuvable.", "error")
            return redirect(url_for("trading.index"))

        price = coin["current_price"]

        if action == "buy":
            _execute_buy(coin_id, quantity, price)
        elif action == "sell":
            _execute_sell(coin_id, quantity, price)
        else:
            flash("Action invalide.", "error")

        return redirect(url_for("trading.index", coin=coin_id))

    selected_coin_id = request.args.get("coin", coins[0]["id"] if coins else None)
    holdings_dict = {h.coin_id: h.quantity for h in current_user.holdings if h.quantity > 0}

    return render_template(
        "trading.html",
        coins=coins,
        selected_coin_id=selected_coin_id,
        holdings_dict=holdings_dict,
        fee_rate=FEE_RATE,
    )


def _execute_buy(coin_id, quantity, price):
    cost = quantity * price
    fee = round(cost * FEE_RATE, 2)
    total_cost = round(cost + fee, 2)

    if current_user.cash_balance < total_cost:
        flash("Solde insuffisant pour cet achat.", "error")
        return

    holding = Holding.query.filter_by(user_id=current_user.id, coin_id=coin_id).first()

    if holding is None:
        holding = Holding(user_id=current_user.id, coin_id=coin_id, quantity=0.0, avg_buy_price=0.0)
        db.session.add(holding)

    new_total_quantity = holding.quantity + quantity
    holding.avg_buy_price = (
        (holding.quantity * holding.avg_buy_price) + (quantity * price)
    ) / new_total_quantity
    holding.quantity = new_total_quantity

    current_user.cash_balance = round(current_user.cash_balance - total_cost, 2)

    db.session.add(Transaction(
        user_id=current_user.id,
        coin_id=coin_id,
        type="buy",
        quantity=quantity,
        price=price,
        fee=fee,
    ))

    db.session.commit()
    flash(f"Achat de {quantity} {coin_id} effectué (frais : ${fee}).", "success")


def _execute_sell(coin_id, quantity, price):
    holding = Holding.query.filter_by(user_id=current_user.id, coin_id=coin_id).first()

    if holding is None or quantity > holding.quantity + 1e-8:
        flash("Quantité détenue insuffisante pour cette vente.", "error")
        return

    proceeds = quantity * price
    fee = round(proceeds * FEE_RATE, 2)
    net_proceeds = round(proceeds - fee, 2)

    holding.quantity -= quantity
    if holding.quantity <= 1e-8:
        db.session.delete(holding)

    current_user.cash_balance = round(current_user.cash_balance + net_proceeds, 2)

    db.session.add(Transaction(
        user_id=current_user.id,
        coin_id=coin_id,
        type="sell",
        quantity=quantity,
        price=price,
        fee=fee,
    ))

    db.session.commit()
    flash(f"Vente de {quantity} {coin_id} effectuée (frais : ${fee}).", "success")
