from flask import render_template, request
from flask_login import login_required, current_user

from app.history import bp
from app.models import Transaction

SORT_FIELDS = {
    "date": Transaction.timestamp,
    "amount": Transaction.quantity * Transaction.price,
}


@bp.route("/history")
@login_required
def index():
    type_filter = request.args.get("type", "all")
    coin_filter = request.args.get("coin", "all")
    sort_by = request.args.get("sort", "date")
    order = request.args.get("order", "desc")

    query = Transaction.query.filter_by(user_id=current_user.id)

    if type_filter in ("buy", "sell"):
        query = query.filter_by(type=type_filter)

    if coin_filter != "all":
        query = query.filter_by(coin_id=coin_filter)

    sort_column = SORT_FIELDS.get(sort_by, Transaction.timestamp)
    query = query.order_by(sort_column.desc() if order == "desc" else sort_column.asc())

    transactions = query.all()

    coin_rows = (
        Transaction.query.filter_by(user_id=current_user.id)
        .with_entities(Transaction.coin_id)
        .distinct()
        .all()
    )
    coin_options = sorted({row[0] for row in coin_rows})

    return render_template(
        "history.html",
        transactions=transactions,
        coin_options=coin_options,
        type_filter=type_filter,
        coin_filter=coin_filter,
        sort_by=sort_by,
        order=order,
    )
