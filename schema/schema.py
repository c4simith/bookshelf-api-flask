"""Schema objects for the app"""
from marshmallow import Schema, fields


class BookSchema(Schema):
    """Book Object with all fields"""
    bookid = fields.Int(required=True)
    title = fields.Str(required=True)
    author = fields.Str(required=True)


class BookSchemaAbstract(Schema):
    """Book object without ID field"""
    title = fields.Str(required=True)
    author = fields.Str(required=True)
