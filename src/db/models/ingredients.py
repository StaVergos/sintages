from typing import List, TYPE_CHECKING
from src.db.base import Base, TimestampMixin
from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

if TYPE_CHECKING:
    from src.db.models.categories import Category
    from src.db.models.recipes import Recipe, RecipeIngredient


class Ingredient(Base, TimestampMixin):
    __tablename__ = "ingredients"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    _name: Mapped[str] = mapped_column(
        String(100), unique=True, nullable=False, name="name"
    )
    is_vegan: Mapped[bool] = mapped_column(nullable=False, default=False)
    categories: Mapped[List["Category"]] = relationship(
        "Category",
        secondary="ingredient_category",
        back_populates="ingredients",
    )
    recipe_ingredients: Mapped[List["RecipeIngredient"]] = relationship(
        "RecipeIngredient",
        back_populates="ingredient",
        cascade="all, delete-orphan",
    )
    recipes: Mapped[List["Recipe"]] = relationship(
        "Recipe",
        secondary="recipe_ingredients",
        back_populates="ingredients",
        overlaps="recipe_ingredients",
    )

    @property
    def name(self) -> str:
        return self._name

    @name.setter
    def name(self, value: str) -> None:
        self._name = value.lower()

    @property
    def category_ids(self) -> List[int]:
        return [category.id for category in self.categories]


class IngredientCategory(Base):
    __tablename__ = "ingredient_category"

    ingredient_id: Mapped[int] = mapped_column(
        ForeignKey("ingredients.id"), primary_key=True
    )
    category_id: Mapped[int] = mapped_column(
        ForeignKey("categories.id"), primary_key=True
    )
