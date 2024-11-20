from marshmallow import Schema, fields

class CustomerMovieSchema(Schema):
  id = fields.Int(dump_only=True)
  customer_id = fields.Int(required=True)
  movie_id = fields.Int(required=True)
  due = fields.DateTime(format='%Y-%m-%d', required=True)
  extended = fields.Bool(required=True)
