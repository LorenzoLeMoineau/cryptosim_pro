from flask import Blueprint

bp = Blueprint("market", __name__)

from app.market import routes  # noqa: E402,F401
