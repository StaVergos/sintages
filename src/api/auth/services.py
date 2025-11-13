from datetime import datetime, timedelta
from typing import Annotated
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
import jwt
from jwt.exceptions import InvalidTokenError
import os
from pytest import Session
from src.api.auth.schemas import TokenData
from src.api.users.schemas import GetUserSchema, UserSchema
from src.core.enums import ErrorKind
from src.core.exceptions import ErrorException
from src.core.security import verify_password
from dotenv import load_dotenv, find_dotenv
from src.db.models.users import User
from src.core.config import config

load_dotenv(find_dotenv())

SECRET_KEY = os.environ.get("SECRET_KEY")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.environ.get("ACCESS_TOKEN_EXPIRE_MINUTES", 30))
ALGORITHM = os.environ.get("ALGORITHM")


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


class UserInDB(UserSchema):
    hashed_password: str


class AuthRepository:
    def __init__(self, db: Session):
        self.db = db

    @property
    def repo_name(self) -> str:
        return "AuthRepository"

    def get_user_by_username(self, username: str) -> GetUserSchema | None:
        user = self.db.query(User).filter(User.username == username).first()
        if user:
            return GetUserSchema.model_validate(user)
        else:
            raise ErrorException(
                code=status.HTTP_404_NOT_FOUND,
                message="User not found",
                kind=ErrorKind.NOT_FOUND,
                source=f"{self.repo_name}.get_user_by_username",
            )

    def authenticate_user(
        self,
        username: str,
        password: str,
    ):
        user = self.get_user_by_username(username)
        if not user:
            return False
        if not verify_password(password, user.hashed_password):
            return False
        return user

    def create_access_token(
        data: TokenData,
        expiration_timestamp: datetime,
        expires_delta: timedelta | None = None,
    ):
        to_encode = data.model_copy()
        if expires_delta:
            expire = expiration_timestamp + expires_delta
        else:
            expire = expiration_timestamp + timedelta(
                minutes=config.ACCESS_TOKEN_EXPIRE_MINUTES
            )
        to_encode.update({"exp": int(expire.timestamp())})
        encoded_jwt = jwt.encode(
            to_encode, config.SECRET_KEY, algorithm=config.ALGORITHM
        )
        return encoded_jwt

    def get_current_user(
        self,
        token: Annotated[str, Depends(oauth2_scheme)],
    ) -> UserSchema:
        credentials_exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            username = payload.get("sub")
            if username is None:
                raise credentials_exception
            token_data = TokenData(username=username)
        except InvalidTokenError:
            raise credentials_exception
        user = self.get_user_by_username(username=token_data.username)
        if user is None:
            raise credentials_exception
        return user

    def get_current_active_user(
        self,
        current_user: Annotated[UserSchema, Depends(get_current_user)],
    ):
        if not current_user.is_active:
            raise HTTPException(status_code=400, detail="Inactive user")
        return current_user
