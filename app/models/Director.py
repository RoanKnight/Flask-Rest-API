from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, Boolean, Integer, ForeignKey
from app import db

class Director(db.Model):
  __tablename__ = 'directors'

  id: Mapped[int] = mapped_column(Integer, primary_key=True)
  website_url: Mapped[str] = mapped_column(String(100), nullable=False)
  user_id: Mapped[int] = mapped_column(
      Integer, ForeignKey('users.id'), nullable=False)
  deleted: Mapped[bool] = mapped_column(Boolean, default=False)

  # One-to-one relationship with User
  user = relationship("User", back_populates="director")
