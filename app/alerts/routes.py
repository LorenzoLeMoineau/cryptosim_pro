from flask import render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user

from app.alerts import bp
from app.extensions import db
from app.models import PriceAlert
from app.market.coingecko import get_market_data


@bp.route("/alerts")
@login_required
def index():
    coins = get_market_data()
    alerts = (
        PriceAlert.query.filter_by(user_id=current_user.id)
        .order_by(PriceAlert.created_at.desc())
        .all()
    )
    return render_template("alerts.html", coins=coins, alerts=alerts)


@bp.route("/alerts/create", methods=["POST"])
@login_required
def create():
    coin_id = request.form.get("coin_id")
    direction = request.form.get("direction")
    target_price_raw = request.form.get("target_price", "")

    try:
        target_price = float(target_price_raw)
    except ValueError:
        flash("Prix cible invalide.", "error")
        return redirect(url_for("alerts.index"))

    if target_price <= 0 or direction not in ("above", "below") or not coin_id:
        flash("Formulaire d'alerte invalide.", "error")
        return redirect(url_for("alerts.index"))

    db.session.add(PriceAlert(
        user_id=current_user.id,
        coin_id=coin_id,
        target_price=target_price,
        direction=direction,
    ))
    db.session.commit()

    condition_text = "au-dessus de" if direction == "above" else "en-dessous de"
    flash(f"Alerte créée : {coin_id} {condition_text} ${target_price}.", "success")
    return redirect(url_for("alerts.index"))


@bp.route("/alerts/<int:alert_id>/delete", methods=["POST"])
@login_required
def delete(alert_id):
    alert = PriceAlert.query.filter_by(id=alert_id, user_id=current_user.id).first()

    if alert is None:
        flash("Alerte introuvable.", "error")
    else:
        db.session.delete(alert)
        db.session.commit()
        flash("Alerte supprimée.", "success")

    return redirect(url_for("alerts.index"))
