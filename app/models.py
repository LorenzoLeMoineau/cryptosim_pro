from datetime import datetime

from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

from app.extensions import db


class User(db.Model, UserMixin):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    cash_balance = db.Column(db.Float, nullable=False, default=10000.0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    holdings = db.relationship("Holding", backref="user", lazy=True, cascade="all, delete-orphan")
    transactions = db.relationship("Transaction", backref="user", lazy=True, cascade="all, delete-orphan")
    watchlist_items = db.relationship("Watchlist", backref="user", lazy=True, cascade="all, delete-orphan")
    price_alerts = db.relationship("PriceAlert", backref="user", lazy=True, cascade="all, delete-orphan")

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f"<User {self.username}>"


class Holding(db.Model):
    __tablename__ = "holdings"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    coin_id = db.Column(db.String(50), nullable=False)
    quantity = db.Column(db.Float, nullable=False, default=0.0)
    avg_buy_price = db.Column(db.Float, nullable=False, default=0.0)

    __table_args__ = (db.UniqueConstraint("user_id", "coin_id", name="uq_user_coin_holding"),)

    def __repr__(self):
        return f"<Holding {self.coin_id} x{self.quantity} (user={self.user_id})>"


class Transaction(db.Model):
    __tablename__ = "transactions"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    coin_id = db.Column(db.String(50), nullable=False)
    type = db.Column(db.String(4), nullable=False)  # "buy" or "sell"
    quantity = db.Column(db.Float, nullable=False)
    price = db.Column(db.Float, nullable=False)
    fee = db.Column(db.Float, nullable=False, default=0.0)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<Transaction {self.type} {self.quantity} {self.coin_id} @ {self.price}>"


class Watchlist(db.Model):
    __tablename__ = "watchlist"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    coin_id = db.Column(db.String(50), nullable=False)

    __table_args__ = (db.UniqueConstraint("user_id", "coin_id", name="uq_user_coin_watchlist"),)

    def __repr__(self):
        return f"<Watchlist {self.coin_id} (user={self.user_id})>"


class PriceAlert(db.Model):
    __tablename__ = "price_alerts"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    coin_id = db.Column(db.String(50), nullable=False)
    target_price = db.Column(db.Float, nullable=False)
    direction = db.Column(db.String(5), nullable=False)  # "above" or "below"
    triggered = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<PriceAlert {self.coin_id} {self.direction} {self.target_price}>"
