from src.db.base import Base, TimestampMixin
from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import List


class Ingredient(Base, TimestampMixin):
    __tablename__ = "ingredients"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    _name: Mapped[str] = mapped_column(
        String(100), unique=True, nullable=False, name="name"
    )
    is_vegan: Mapped[bool] = mapped_column(nullable=False, default=False)
    category_id: Mapped[int] = mapped_column(ForeignKey("categories.id"))
    category: Mapped[List["Category"]] = relationship(back_populates="Ingredient")  # noqa: F821

    @property
    def name(self) -> str:
        return self._name

    @name.setter
    def name(self, value: str) -> None:
        self._name = value.lower()
