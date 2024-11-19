from marshmallow import Schema, fields
from app.models.User import UserRole

class UserSchema(Schema):
  id = fields.Int(dump_only=True)
  name = fields.Str(required=True)
  email = fields.Email(required=True)
  phone_number = fields.Str()
  address = fields.Str()
  role = fields.Enum(
      UserRole,
      by_value=True,
      missing=UserRole.CUSTOMER.value,
      required=False
  )
  deleted = fields.Bool(dump_only=True)
  password = fields.Str(load_only=True, required=True)
  c_password = fields.Str(load_only=True, required=True)
