"""Blueprint module to handle API endpoints on Book operations"""
from flask import request
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from sqlalchemy.exc import SQLAlchemyError
from schema.schema import BookSchema, BookSchemaAbstract
from model.book import BookModel
from database.db import db


blueprint = Blueprint("books", __name__, description="Operations on book resources")


@blueprint.route("/books")
class Books(MethodView):
    """Endpoints for book resource, includes Create and Read operations"""

    @blueprint.response(200, BookSchema(many=True))
    def get(self):
        return BookModel.query.limit(10).all()

    @blueprint.arguments(BookSchemaAbstract)
    @blueprint.response(201, BookSchema)
    def post(self, request_data):
        try:
            book = BookModel(**request_data)
            db.session.add(book)
            db.session.commit()
            return book
        except SQLAlchemyError:
            abort(500, message="Error during database operation")


@blueprint.route("/books/<int:bookid>")
class BookByID(MethodView):
    """Endpoints point for book operation based on Book ID. Includes Read, Update, Delete operations"""

    @blueprint.response(200, BookSchema)
    def get(self, bookid):
        return BookModel.query.get_or_404(bookid)

    @blueprint.arguments(BookSchemaAbstract)
    @blueprint.response(200, BookSchema)
    def put(self, request_data, bookid):
        try:
            book = BookModel.query.get(bookid)
            if book is None:
                abort(400, message="Book with given id does not exists")
            else:
                book.title = request_data["title"]
                book.author = request_data["author"]
                db.session.add(book)
                db.session.commit()
                return book
        except SQLAlchemyError:
            abort(500, message="Error during database operation")

    @blueprint.response(200, BookSchema)
    def delete(self, bookid):
        try:
            book = BookModel.query.get(bookid)
            if book is None:
                abort(400, message="Book with given id does not exists")
            else:
                db.session.delete(book)
                db.session.commit()
                return book
        except SQLAlchemyError:
            abort(500, message="Error during database operation")


@blueprint.route("/books/search")
class BookSearch(MethodView):
    """Endpoints for searching books in the bookshelf. Includes search by title or author"""

    @blueprint.response(200, BookSchemaAbstract(many=True))
    def get(self):
        queryparams = list(request.args)
        if len(queryparams) == 1:
            match queryparams[0]:
                case "title":
                    title = request.args.get("title")
                    return BookModel.query.filter(BookModel.title.contains(title))
                case "author":
                    author = request.args.get("author")
                    return BookModel.query.filter(BookModel.author.contains(author))
                case _:
                    abort(400, message="Invalid search request")
        else:
            abort(400, message="Invalid search request")
