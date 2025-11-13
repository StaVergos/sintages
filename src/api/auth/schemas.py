from pydantic import BaseModel
from datetime import datetime, timezone


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str
    expiration_timestamp: datetime = datetime.now(timezone.utc)
