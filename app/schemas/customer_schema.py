from marshmallow import Schema, fields

class CustomerSchema(Schema):
  id = fields.Int()
  date_of_birth = fields.Date()
  user_id = fields.Int()
  deleted = fields.Bool()
