from datetime import datetime
from pydantic import Field, EmailStr
from src.api.schemas import BaseSchema


class UserSchema(BaseSchema):
    username: str = Field(..., examples=["johndoe"])
    email: EmailStr = Field(..., examples=["johndoe@example.com"])
    full_name: str = Field(..., examples=["John Doe"])
    is_active: bool = Field(..., examples=[True])


class CreateUserSchema(UserSchema):
    password: str = Field(..., min_length=8, examples=["strongpassword123"])


class UpdateUserSchema(UserSchema):
    username: str | None = Field(examples=["johndoe"], default=None)
    email: EmailStr | None = Field(examples=["johndoe@example.com"], default=None)
    full_name: str | None = Field(examples=["John Doe"], default=None)
    is_active: bool | None = Field(examples=[True], default=None)


class GetUserSchema(UserSchema):
    id: int = Field(..., examples=[1])
    created_at: datetime = Field(..., examples=["2023-10-01T12:00:00Z"])
    updated_at: datetime | None = Field(examples=["2023-10-01T12:00:00Z"], default=None)
