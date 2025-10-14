from datetime import datetime
from pydantic import Field, field_validator, field_serializer
from src.api.schemas import BaseSchema


class CategorySchema(BaseSchema):
    name: str = Field(max_length=50, examples=["Fruits"])

    @field_validator("name")
    def validate_name(cls, value: str) -> str:
        return value.lower()

    @field_serializer("name")
    def serialize_name(self, value: str) -> str:
        return value.capitalize()


class GetCategorySchema(CategorySchema):
    id: int = Field(..., examples=[1])
    updated_at: datetime = Field(..., examples=["2023-10-01T12:00:00Z"])


class CreateCategorySchema(CategorySchema):
    created_at: datetime = Field(..., examples=["2023-10-01T12:00:00Z"])


class UpdateCategorySchema(CategorySchema):
    name: str | None = Field(examples=["Fruits"], default=None)