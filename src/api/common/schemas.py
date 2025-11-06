from datetime import datetime
from pydantic import Field, field_validator, field_serializer
from src.api.schemas import BaseSchema


class IngredientSchema(BaseSchema):
    name: str = Field(max_length=50, examples=["Broccoli"])
    is_vegan: bool = Field(..., examples=[True])
    categories: list["CategoryRelationshipSchema"] = Field(
        default_factory=list,
        examples=[[{"id": 1, "name": "Veggies"}]],
    )

    @field_validator("name")
    @classmethod
    def validate_name(cls, value: str) -> str:
        return value.lower()

    @field_serializer("name")
    def serialize_name(self, value: str) -> str:
        return value.capitalize()


class GetIngredientSchema(IngredientSchema):
    id: int = Field(..., examples=[1])
    created_at: datetime = Field(..., examples=["2023-10-01T12:00:00Z"])
    updated_at: datetime | None = Field(..., examples=["2023-10-01T12:00:00Z"])


class CreateIngredientSchema(IngredientSchema):
    pass


class UpdateIngredientSchema(IngredientSchema):
    name: str | None = Field(examples=["Broccoli"], default=None)
    is_vegan: bool | None = Field(examples=[True], default=None)
    categories: list["CategoryRelationshipSchema"] = Field(
        default_factory=list,
        examples=[[{"id": 1, "name": "Veggies"}]],
    )


class IngredientRelationshipSchema(BaseSchema):
    id: int = Field(..., examples=[1])
    name: str = Field(max_length=50, examples=["Broccoli"])


class CategorySchema(BaseSchema):
    name: str = Field(max_length=50, examples=["Veggies"])

    @field_validator("name")
    @classmethod
    def validate_name(cls, value: str) -> str:
        return value.lower()

    @field_serializer("name")
    def serialize_name(self, value: str) -> str:
        return value.capitalize()


class GetCategorySchema(CategorySchema):
    id: int = Field(..., examples=[1])
    created_at: datetime = Field(..., examples=["2023-10-01T12:00:00Z"])
    updated_at: datetime | None = Field(..., examples=["2023-10-01T12:00:00Z"])
    ingredients: list["IngredientRelationshipSchema"] = Field(
        default_factory=list,
        examples=[[{"id": 1, "name": "Broccoli"}]],
    )


class CreateCategorySchema(CategorySchema):
    pass


class UpdateCategorySchema(CategorySchema):
    name: str | None = Field(examples=["Veggies"], default=None)


class CategoryRelationshipSchema(BaseSchema):
    id: int = Field(..., examples=[1])
    name: str = Field(max_length=50, examples=["Veggies"])
