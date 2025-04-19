from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from app.config import Settings

db = SQLAlchemy()

def create_app():

    app = Flask(__name__)
    app.config.from_object(Settings)

    db.init_app(app)

    app.config["SECRET_KEY"] = config.SECRET_KEY
    app.config["SQLALCHEMY_DATABASE_URI"] = config.SQLALCHEMY_DATABASE_URI
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.init_app(app)

    return app
