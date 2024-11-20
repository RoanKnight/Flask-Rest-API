from marshmallow import Schema, fields

class CustomerSchema(Schema):
  id = fields.Int(dump_only=True)
  date_of_birth = fields.Date(required=True)
  user_id = fields.Int(required=True)
  deleted = fields.Bool(dump_only=True)
