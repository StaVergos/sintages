from pydantic import BaseModel
from datetime import datetime


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str
    expiration_timestamp: datetime


class LoginRequest(BaseModel):
    username: str
    password: str


class JWTData(BaseModel):
    username: str
    expire: datetime
    type: str = "Bearer"
