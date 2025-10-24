from typing import List, TYPE_CHECKING
from src.db.base import Base, TimestampMixin
from sqlalchemy import String, ForeignKey, Enum as sqlenum
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.ext.associationproxy import association_proxy
from src.db.models.users import User
from src.api.recipes.enums import DifficultyLevel

if TYPE_CHECKING:
    from src.db.models.ingredients import Ingredient


class Recipe(Base, TimestampMixin):
    __tablename__ = "recipes"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    _name: Mapped[str] = mapped_column(
        String(183), unique=True, nullable=False, name="name"
    )
    cooking_time: Mapped[int] = mapped_column(nullable=False)
    difficulty_level: Mapped[DifficultyLevel] = mapped_column(
        sqlenum(DifficultyLevel), nullable=False
    )
    portions: Mapped[int] = mapped_column(nullable=False)
    instructions: Mapped[str] = mapped_column(nullable=False)
    recipe_ingredients = relationship(
        "RecipeIngredient",
        back_populates="recipe",
        cascade="all, delete-orphan",
        overlaps="ingredients",
    )
    ingredients: Mapped[List["Ingredient"]] = relationship(
        "Ingredient",
        secondary="recipe_ingredients",
        back_populates="recipes",
        overlaps="recipe_ingredients",
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

    @property
    def ingredient_ids(self) -> List[int]:
        return [ingredient.id for ingredient in self.ingredients]

    @property
    def recipe_ingredients_payload(self) -> List[dict]:
        return [
            {"ingredient_id": assoc.ingredient_id, "quantity": assoc.quantity}
            for assoc in self.recipe_ingredients
        ]

    @property
    def is_vegan(self) -> bool:
        return all(ingredient.is_vegan for ingredient in self.ingredients)


class RecipeIngredient(Base):
    __tablename__ = "recipe_ingredients"
    recipe_id: Mapped[int] = mapped_column(ForeignKey("recipes.id"), primary_key=True)
    ingredient_id: Mapped[int] = mapped_column(
        ForeignKey("ingredients.id"), primary_key=True
    )
    quantity: Mapped[str] = mapped_column(nullable=False)
    recipe: Mapped["Recipe"] = relationship(
        back_populates="recipe_ingredients", overlaps="ingredients,recipes"
    )
    ingredient: Mapped["Ingredient"] = relationship(
        back_populates="recipe_ingredients", overlaps="ingredients,recipes"
    )

    __mapper_args__ = {"confirm_deleted_rows": False}
