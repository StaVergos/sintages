from typing import List, TYPE_CHECKING
from src.db.base import Base, TimestampMixin
from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.ext.associationproxy import association_proxy
from src.db.models.users import User

if TYPE_CHECKING:
    from src.db.models.ingredients import Ingredient


class Recipe(Base, TimestampMixin):
    __tablename__ = "recipes"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    _name: Mapped[str] = mapped_column(
        String(183), unique=True, nullable=False, name="name"
    )
    cooking_time: Mapped[int] = mapped_column(nullable=False)
    difficulty_level: Mapped[str] = mapped_column(
        nullable=False,
    )
    portions: Mapped[int] = mapped_column(nullable=False)
    is_vegan: Mapped[bool] = mapped_column(nullable=False, default=False)
    instructions: Mapped[str] = mapped_column(nullable=False)
    recipe_ingredients = relationship("RecipeIngredient", back_populates="recipe")
    ingredients: Mapped[List["Ingredient"]] = relationship(
        "Ingredient", secondary="recipe_ingredients", back_populates="recipe"
    )
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    user: Mapped["User"] = relationship(back_populates="recipes")
    quantity = association_proxy(
        target_collection="recipe_ingredients", attr="quantity"
    )

    @property
    def name(self) -> str:
        return self._name

    @name.setter
    def name(self, value: str) -> None:
        self._name = value.lower()


class RecipeIngredient(Base):
    __tablename__ = "recipe_ingredients"
    recipe_id: Mapped[int] = mapped_column(ForeignKey("recipes.id"), primary_key=True)
    ingredient_id: Mapped[int] = mapped_column(
        ForeignKey("ingredients.id"), primary_key=True
    )
    quantity: Mapped[str] = mapped_column(nullable=False)
    recipe: Mapped["Recipe"] = relationship(back_populates="recipe_ingredients")
    ingredient: Mapped["Ingredient"] = relationship(back_populates="recipe_ingredients")
