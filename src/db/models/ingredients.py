from typing import Optional
from src.db.base import Base, TimestampMixin
from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from src.db.models.categories import Category
from src.db.models.recipes import Recipe


class Ingredient(Base, TimestampMixin):
    __tablename__ = "ingredients"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    _name: Mapped[str] = mapped_column(
        String(100), unique=True, nullable=False, name="name"
    )
    is_vegan: Mapped[bool] = mapped_column(nullable=False, default=False)
    category_id: Mapped[Optional[int]] = mapped_column(
        ForeignKey("categories.id"), nullable=True
    )
    category: Mapped["Category"] = relationship(back_populates="ingredients")
    recipe_id: Mapped[Optional[int]] = mapped_column(
        ForeignKey("recipes.id"), nullable=True
    )
    recipe: Mapped["Recipe"] = relationship(back_populates="ingredients")

    @property
    def name(self) -> str:
        return self._name

    @name.setter
    def name(self, value: str) -> None:
        self._name = value.lower()
