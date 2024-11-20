from marshmallow import Schema, fields

class DirectorSchema(Schema):
  id = fields.Int(dump_only=True)
  website_url = fields.Str(required=True)
  user_id = fields.Int(required=True)
  deleted = fields.Bool(dump_only=True)
