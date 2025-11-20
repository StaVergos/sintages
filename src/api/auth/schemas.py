from pydantic import BaseModel
from datetime import datetime

from src.api.auth.enums import JWTType


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
    type: JWTType
