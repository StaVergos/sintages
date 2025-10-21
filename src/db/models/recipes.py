from typing import Optional, List, TYPE_CHECKING
from src.db.base import Base, TimestampMixin
from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
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
    ingredients: Mapped[List["Ingredient"]] = relationship(back_populates="recipe")
    user_id: Mapped[Optional[int]] = mapped_column(
        ForeignKey("users.id"), nullable=True
    )
    user: Mapped["User"] = relationship(back_populates="recipes")

    @property
    def name(self) -> str:
        return self._name

    @name.setter
    def name(self, value: str) -> None:
        self._name = value.lower()
