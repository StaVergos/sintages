from src.db.base import Base, TimestampMixin
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column


class Ingredient(Base, TimestampMixin):
    __tablename__ = "ingredients"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    _name: Mapped[str] = mapped_column(
        String(100), unique=True, nullable=False, name="name"
    )
    is_vegan: Mapped[bool] = mapped_column(nullable=False, default=False)

    @property
    def name(self) -> str:
        return self._name

    @name.setter
    def name(self, value: str) -> None:
        self._name = value.lower()
