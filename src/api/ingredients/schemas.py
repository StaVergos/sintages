from datetime import datetime
from pydantic import Field, field_validator, field_serializer, model_validator
from src.api.schemas import BaseSchema


class IngredientSchema(BaseSchema):
    name: str = Field(max_length=50, examples=["Broccoli"])
    is_vegan: bool = Field(..., examples=[True])
    category_ids: list[int] = Field(default_factory=list, examples=[[1]])

    @field_validator("name")
    @classmethod
    def validate_name(cls, value: str) -> str:
        return value.lower()

    @field_serializer("name")
    def serialize_name(self, value: str) -> str:
        return value.capitalize()

    @model_validator(mode="before")
    @classmethod
    def extract_category_ids(cls, data):
        if isinstance(data, dict) and "categories" in data and "category_ids" not in data:
            categories = data.get("categories") or []
            data = {**data}
            data["category_ids"] = [cat.id if hasattr(cat, "id") else cat for cat in categories]
        return data

    @field_serializer("category_ids", when_used="json")
    def serialize_category_ids(self, value: list[int]) -> list[int]:
        return value or []


class GetIngredientSchema(IngredientSchema):
    id: int = Field(..., examples=[1])
    created_at: datetime = Field(..., examples=["2023-10-01T12:00:00Z"])
    updated_at: datetime | None = Field(..., examples=["2023-10-01T12:00:00Z"])


class CreateIngredientSchema(IngredientSchema):
    pass


class UpdateIngredientSchema(IngredientSchema):
    name: str | None = Field(examples=["Broccoli"], default=None)
    is_vegan: bool | None = Field(examples=[True], default=None)
    category_ids: list[int] | None = Field(default=None, examples=[[1]])
