from flask import render_template, redirect, url_for, request, flash
from flask_login import login_required, current_user

from app.watchlist import bp
from app.extensions import db
from app.models import Watchlist
from app.market.coingecko import get_market_data


@bp.route("/watchlist")
@login_required
def index():
    watched_coin_ids = {w.coin_id for w in current_user.watchlist_items}
    coins = [c for c in get_market_data() if c["id"] in watched_coin_ids]

    return render_template("watchlist.html", coins=coins)


@bp.route("/watchlist/toggle", methods=["POST"])
@login_required
def toggle():
    coin_id = request.form.get("coin_id")

    if not coin_id:
        flash("Cryptomonnaie invalide.", "error")
        return redirect(request.referrer or url_for("market.index"))

    existing = Watchlist.query.filter_by(user_id=current_user.id, coin_id=coin_id).first()

    if existing:
        db.session.delete(existing)
        db.session.commit()
        flash(f"{coin_id} retiré de votre watchlist.", "success")
    else:
        db.session.add(Watchlist(user_id=current_user.id, coin_id=coin_id))
        db.session.commit()
        flash(f"{coin_id} ajouté à votre watchlist.", "success")

    return redirect(request.referrer or url_for("market.index"))
