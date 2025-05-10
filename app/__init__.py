from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from app.database.config import settings

db = SQLAlchemy()


def create_app():
    app = Flask(__name__)
    app.config.from_object(settings)

    db.init_app(app)

    app.config["SECRET_KEY"] = settings.SECRET_KEY
    app.config["SQLALCHEMY_DATABASE_URI"] = settings.SQLALCHEMY_DATABASE_URI
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.init_app(app)

    return app
