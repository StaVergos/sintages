from src.db.base import Base, TimestampMixin
from sqlalchemy import String, Integer
from sqlalchemy.orm import Mapped, mapped_column


class User(Base, TimestampMixin):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    username: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    email: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    full_name: Mapped[str | None] = mapped_column(String(100), nullable=True)
    hashed_password: Mapped[str] = mapped_column(String(255), nullable=False)
    is_active: Mapped[bool] = mapped_column(default=True, nullable=False)


class Ingredient(Base, TimestampMixin):
    __tablename__ = "ingredients"

    ing_id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    ing_name: Mapped[str | None] = mapped_column(String(100), nullable=False)
    ing_amount: Mapped[int] = mapped_column(Integer, nullable=False)
    ing_grams: Mapped[int] = mapped_column(Integer, nullable=False)
    ing_category: Mapped[str | None] = mapped_column(String(100), nullable=False)
