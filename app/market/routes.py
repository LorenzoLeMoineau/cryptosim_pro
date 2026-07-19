from flask import render_template
from flask_login import login_required

from app.market import bp
from app.market.coingecko import get_market_data


@bp.route("/market")
@login_required
def index():
    coins = get_market_data()
    return render_template("market.html", coins=coins)
