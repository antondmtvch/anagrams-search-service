from marshmallow import Schema, fields, validate


class LoadBodyData(Schema):
    words = fields.List(fields.String(), required=True, validate=validate.Length(1, 100))
