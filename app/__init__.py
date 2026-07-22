import os
from flask import Flask, render_template, request, flash
from config import Config
from app.extensions import db, login_manager


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    os.makedirs(os.path.join(app.root_path, "..", "instance"), exist_ok=True)

    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = "auth.login"

    from app import models

    @login_manager.user_loader
    def load_user(user_id):
        return models.User.query.get(int(user_id))

    with app.app_context():
        db.create_all()

    from app.auth import bp as auth_bp
    app.register_blueprint(auth_bp, url_prefix="/auth")

    from app.dashboard import bp as dashboard_bp
    app.register_blueprint(dashboard_bp)

    from app.market import bp as market_bp
    app.register_blueprint(market_bp)

    from app.trading import bp as trading_bp
    app.register_blueprint(trading_bp)

    from app.portfolio import bp as portfolio_bp
    app.register_blueprint(portfolio_bp)

    from app.history import bp as history_bp
    app.register_blueprint(history_bp)

    from app.leaderboard import bp as leaderboard_bp
    app.register_blueprint(leaderboard_bp)

    from app.watchlist import bp as watchlist_bp
    app.register_blueprint(watchlist_bp)

    from app.alerts import bp as alerts_bp
    app.register_blueprint(alerts_bp)

    from app.profile import bp as profile_bp
    app.register_blueprint(profile_bp)

    from app.news import bp as news_bp
    app.register_blueprint(news_bp)

    from flask_login import current_user

    @app.context_processor
    def inject_sidebars():
        if not current_user.is_authenticated:
            return {}
        from app.news.rss import get_latest_articles
        from app.market.coingecko import get_market_data
        return {
            "sidebar_articles": get_latest_articles(limit=100),
            "sidebar_coins": get_market_data(),
        }

    @app.before_request
    def check_alerts_globally():
        if request.endpoint == "static" or not current_user.is_authenticated:
            return
        from app.alerts.checks import check_price_alerts
        for alert in check_price_alerts(current_user):
            condition_text = "dépassé" if alert.direction == "above" else "chuté sous"
            flash(f"{alert.coin_id} a {condition_text} ${alert.target_price}.", "price_alert")

    @app.route("/")
    def index():
        return render_template("landing.html")

    @app.errorhandler(404)
    def not_found(error):
        return render_template("errors/404.html"), 404

    @app.errorhandler(500)
    def server_error(error):
        return render_template("errors/500.html"), 500

    return app
