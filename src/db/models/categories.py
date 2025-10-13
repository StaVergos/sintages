from src.db.base import Base, TimestampMixin
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import List


class Category(Base, TimestampMixin):
    __tablename__ = "categories"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    _name: Mapped[str] = mapped_column(
        String(100), unique=True, nullable=False, name="name"
    )
    ingredients: Mapped[List["Ingredient"]] = relationship(back_populates="category")  # noqa: F821

    @property
    def name(self) -> str:
        return self._name

    @name.setter
    def name(self, value: str) -> None:
        self._name = value.lower()
