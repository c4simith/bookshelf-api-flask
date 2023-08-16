"""API Start point, includes the configuration initilaization and database setup"""
from flask import Flask
from flask_smorest import Api
from blueprint.books import blueprint as books_blueprint
from database.db import db
from model.book import BookModel


def create_app():
    """Create, initialize and return the app object"""
    app = Flask(__name__)
    app.config["API_TITLE"] = "Bookshelf API"
    app.config["API_VERSION"] = "v1"
    app.config["OPENAPI_VERSION"] = "3.1.0"
    app.config["OPENAPI_URI_PREFIX"] = "/"
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///bookshelf.db"
    db.init_app(app)
    with app.app_context():
        db.create_all()

    api = Api(app)
    api.register_blueprint(books_blueprint)
    return app
