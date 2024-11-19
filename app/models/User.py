from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, Boolean, Integer, ForeignKey
from werkzeug.security import generate_password_hash, check_password_hash
import enum
import re
from app import db
from sqlalchemy import Enum as SAEnum

class UserRole(enum.Enum):
  CUSTOMER = "Customer"
  DIRECTOR = "Director"

class User(db.Model):
  __tablename__ = 'users'

  id: Mapped[int] = mapped_column(Integer, primary_key=True)
  name: Mapped[str] = mapped_column(String(100), nullable=False)
  email: Mapped[str] = mapped_column(
      String(120), unique=True, nullable=False, index=True)
  password_hash: Mapped[str] = mapped_column(String(128), nullable=False)
  phone_number: Mapped[str] = mapped_column(String(20), nullable=True)
  address: Mapped[str] = mapped_column(String(200), nullable=True)
  role: Mapped[UserRole] = mapped_column(
      SAEnum(UserRole, values_callable=lambda x: [
             e.value for e in x], name='userrole'),
      nullable=False,
      default=UserRole.CUSTOMER.value
  )
  deleted: Mapped[bool] = mapped_column(Boolean, default=False)

  # One-to-one relationships
  customer = relationship("Customer", uselist=False, back_populates="user")
  director = relationship("Director", uselist=False, back_populates="user")

  def set_password(self, password: str) -> None:
    self.password_hash = generate_password_hash(password)

  def check_password(self, password: str) -> bool:
    return check_password_hash(self.password_hash, password)

  def __repr__(self) -> str:
    return f'<User {self.name}>'

  @staticmethod
  def validate_email(email: str) -> bool:
    email_regex = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
    return re.match(email_regex, email) is not None
