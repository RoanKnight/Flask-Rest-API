from marshmallow import Schema, fields

class MovieSchema(Schema):
  id = fields.Int(dump_only=True)
  title = fields.Str(required=True)
  duration = fields.Int(required=True)
  rating = fields.Int(required=True)
  year = fields.Int(required=True)
  director_id = fields.Int(required=True)
  deleted = fields.Bool(dump_only=True)
