from pydantic import Field
from src.api.schemas import BaseSchema


class IngredientRelationshipSchema(BaseSchema):
    id: int = Field(..., examples=[1])
    name: str = Field(max_length=50, examples=["Broccoli"])


class CategoryRelationshipSchema(BaseSchema):
    id: int = Field(..., examples=[1])
    name: str = Field(max_length=50, examples=["Veggies"])
