from datetime import datetime
from pydantic import Field, field_validator, field_serializer
from src.api.recipes.enums import DifficultyLevel
from src.api.schemas import BaseSchema


class RecipeSchema(BaseSchema):
    name: str = Field(max_length=183, examples=["Tzatziki"])
    cooking_time: int = Field(..., examples=[30], nullable=False)
    difficulty_level: DifficultyLevel = Field(
        ..., examples=["Easy", "Medium", "Hard"], nullable=False
    )
    portions: int = Field(..., examples=[4], nullable=False)
    is_vegan: bool = Field(..., examples=[False])
    instructions: list[str] = Field(..., examples=["Mix all ingredients."])
    ingredients: list[str] = Field(..., examples=["Cucumber", "Egg"], nullable=False)
    quantity: list[str] = Field(..., examples=["200 grams", "1"], nullable=False)
    user_id: int = Field(..., examples=[1], nullable=False)

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
