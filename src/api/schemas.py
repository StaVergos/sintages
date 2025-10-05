from pydantic import BaseModel, ConfigDict, Field


class BaseSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)


class IngredientSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    name: str = Field(max_length=50, examples=["Broccoli"])
    is_vegan: bool = Field(..., examples=[True])


class GetIngredientSchema(IngredientSchema):
    id: int = Field(..., examples=[1])


class CreateIngredientSchema(IngredientSchema):
    pass
