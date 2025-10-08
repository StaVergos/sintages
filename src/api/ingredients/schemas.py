from datetime import datetime
from pydantic import Field
from src.api.schemas import BaseSchema


class IngredientSchema(BaseSchema):
    name: str = Field(max_length=50, examples=["Broccoli"])
    is_vegan: bool = Field(..., examples=[True])


class GetIngredientSchema(IngredientSchema):
    id: int = Field(..., examples=[1])
    created_at: datetime = Field(..., examples=["2023-10-01T12:00:00Z"])


class CreateIngredientSchema(IngredientSchema):
    pass
