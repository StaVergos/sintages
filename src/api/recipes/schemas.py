from datetime import datetime
from pydantic import Field, field_validator, field_serializer
from typing import Literal
from src.api.schemas import BaseSchema


class RecipeSchema(BaseSchema):
    name: str = Field(max_length=183, examples=["Tzatziki"])
    cooking_time: int = Field(..., examples=[30])
    difficulty_level: Literal["Easy", "Medium", "Hard"] = Field(..., examples=["Easy"])
    portions: int = Field(..., examples=[4])
    is_vegan: bool = Field(..., examples=[False])
    instructions: list[str] = Field(..., examples=["Mix all ingredients."])
    ingredient_ids: list[int] | None = Field(..., examples=[[1, 2, 3]])
    user_id: int | None = Field(examples=[1], default=None)

    @field_validator("name")
    @classmethod
    def validate_name(cls, value: str) -> str:
        return value.lower()

    @field_serializer("name")
    def serialize_name(self, value: str) -> str:
        return value.capitalize()


class GetRecipeSchema(RecipeSchema):
    id: int = Field(..., examples=[1])
    created_at: datetime = Field(..., examples=["2023-10-01T12:00:00Z"])


class CreateRecipeSchema(RecipeSchema):
    pass


class DeleteRecipeSchema(RecipeSchema):
    id: int = Field(..., examples=[1])
