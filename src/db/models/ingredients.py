from src.db.base import Base, TimestampMixin
from sqlalchemy import String, Integer
from sqlalchemy.orm import Mapped, mapped_column


class Ingredient(Base, TimestampMixin):
    __tablename__ = "ingredients"

    ing_id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    ing_name: Mapped[str | None] = mapped_column(String(100), nullable=False)
    ing_amount: Mapped[int] = mapped_column(Integer, nullable=False)
    ing_grams: Mapped[int] = mapped_column(Integer, nullable=False)
    ing_category: Mapped[str | None] = mapped_column(String(100), nullable=False)
