from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, Boolean, Integer, ForeignKey, Date
from app import db
from datetime import date

class Customer(db.Model):
  __tablename__ = 'customers'

  id: Mapped[int] = mapped_column(Integer, primary_key=True)
  date_of_birth: Mapped[date] = mapped_column(
      Date, nullable=False)
  user_id: Mapped[int] = mapped_column(
      Integer, ForeignKey('users.id'), nullable=False)
  deleted: Mapped[bool] = mapped_column(Boolean, default=False)

  # One-to-one relationship with User
  user = relationship("User", back_populates="customer")
