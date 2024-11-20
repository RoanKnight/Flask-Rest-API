from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, Boolean, Integer, ForeignKey
from app import db

class Movie(db.Model):
  __tablename__ = 'movies'

  id: Mapped[int] = mapped_column(Integer, primary_key=True)
  title: Mapped[str] = mapped_column(String(100), nullable=False)
  duration: Mapped[int] = mapped_column(Integer, nullable=False)
  rating: Mapped[int] = mapped_column(Integer, nullable=False)
  year: Mapped[int] = mapped_column(Integer, nullable=False)
  director_id: Mapped[int] = mapped_column(
      Integer, ForeignKey('directors.id'), nullable=False)
  deleted: Mapped[bool] = mapped_column(Boolean, default=False)

  # Relationships
  director = relationship("Director", back_populates="movies")
  customers = relationship(
      "Customer", secondary="customer_movies", back_populates="movies")
