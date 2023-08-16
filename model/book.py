from database.db import db


class BookModel(db.Model):
    __tablename__ = "books"
    bookid = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    author = db.Column(db.String, nullable=False)
