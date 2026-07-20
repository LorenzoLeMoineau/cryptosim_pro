from flask import Blueprint

bp = Blueprint("news", __name__)

from app.news import routes  # noqa: E402,F401
