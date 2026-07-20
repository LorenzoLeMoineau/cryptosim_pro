from flask import render_template
from flask_login import login_required, current_user

from app.market import bp
from app.market.coingecko import get_market_data


@bp.route("/market")
@login_required
def index():
    coins = get_market_data()
    watched_coin_ids = {w.coin_id for w in current_user.watchlist_items}
    return render_template("market.html", coins=coins, watched_coin_ids=watched_coin_ids)
