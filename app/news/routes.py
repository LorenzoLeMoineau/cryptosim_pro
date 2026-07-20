from flask import render_template
from flask_login import login_required

from app.news import bp
from app.news.rss import get_latest_articles


@bp.route("/news")
@login_required
def index():
    articles = get_latest_articles()
    return render_template("news.html", articles=articles)
