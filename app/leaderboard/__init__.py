from flask import Blueprint

bp = Blueprint("leaderboard", __name__)

from app.leaderboard import routes  # noqa: E402,F401
