from flask import Blueprint

bp = Blueprint("history", __name__)

from app.history import routes  # noqa: E402,F401
