import os
from flask import Flask
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

    @app.route("/")
    def index():
        return "CryptoSim Pro — projet en cours de construction"

    return app
