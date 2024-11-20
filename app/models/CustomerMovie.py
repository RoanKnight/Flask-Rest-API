from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import Boolean, Integer, ForeignKey, Date
from app import db
from datetime import date

class CustomerMovie(db.Model):
  __tablename__ = 'customer_movies'

  id: Mapped[int] = mapped_column(Integer, primary_key=True)
  customer_id: Mapped[int] = mapped_column(
      Integer, ForeignKey('customers.id'), nullable=False)
  movie_id: Mapped[int] = mapped_column(
      Integer, ForeignKey('movies.id'), nullable=False)
  due: Mapped[date] = mapped_column(Date, nullable=False)
  extended: Mapped[bool] = mapped_column(Boolean, default=False)
  deleted: Mapped[bool] = mapped_column(Boolean, default=False)
