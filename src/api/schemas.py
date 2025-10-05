from pydantic import BaseModel, EmailStr, ConfigDict, Field


class UserSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    username: str = Field(..., examples=["johndoe"])
    email: EmailStr = Field(..., examples=["johndoe@example.com"])
    full_name: str = Field(..., examples=["John Doe"])
    is_active: bool = Field(..., examples=[True])


class CreateUserSchema(UserSchema):
    password: str = Field(..., min_length=8, examples=["strongpassword123"])


class UpdateUserSchema(UserSchema):
    pass


class GetUserSchema(UserSchema):
    id: int = Field(..., examples=[1])


class IngredientSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    name: str = Field(max_length=50, examples=["Broccoli"])
    quantity: int = Field(ge=0, examples=[2])
    grams: int = Field(ge=0, examples=[250])
    category: str = Field(max_length=50, examples=["Vegetables"])


class GetIngredientSchema(IngredientSchema):
    id: int = Field(..., examples=[1])


class CreateIngredientSchema(IngredientSchema):
    pass
