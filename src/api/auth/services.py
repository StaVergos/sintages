from datetime import datetime, timedelta
import logging
from typing import Annotated, Literal
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
import jwt
from src.api.users.schemas import UserSchema
from src.core.security import verify_password
from src.db.models.users import User
from src.core.config import config

logger = logging.getLogger(__name__)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


def create_credentials_exception(detail: str) -> HTTPException:
    return HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail=detail,
        headers={"WWW-Authenticate": "Bearer"},
    )


def confirm_token_expire_minutes() -> int:
    return 1440


def create_access_token(username: str):
    expire = datetime.now(datetime.utc) + timedelta(config.ACCESS_TOKEN_EXPIRE_MINUTES)
    jwt_data = {"sub": username, "exp": expire, "type": "access"}
    encoded_jwt = jwt.encode(
        jwt_data, key=config.SECRET_KEY, algorithm=config.ALGORITHM
    )
    return encoded_jwt


def create_confirmation_token(email: str):
    logger.debug("Creating confirmation token", extra={"email": email})
    expire = datetime.now(datetime.utc) + timedelta(
        minutes=confirm_token_expire_minutes()
    )
    jwt_data = {"sub": email, "exp": expire, "type": "confirmation"}
    encoded_jwt = jwt.encode(
        jwt_data, key=config.SECRET_KEY, algorithm=config.ALGORITHM
    )
    return encoded_jwt


def get_subject_for_token_type(
    token: str, type: Literal["access", "confirmation"]
) -> str:
    try:
        payload = jwt.decode(
            token, key=config.SECRET_KEY, algorithms=[config.ALGORITHM]
        )
    except jwt.ExpiredSignatureError as e:
        raise create_credentials_exception("Token has expired") from e
    except jwt.PyJWTError as e:
        raise create_credentials_exception("Invalid token") from e

    email = payload.get("sub")
    if email is None:
        raise create_credentials_exception("Token is missing 'sub' field")

    token_type = payload.get("type")
    if token_type is None or token_type != type:
        raise create_credentials_exception(
            f"Token has incorrect type, expected '{type}'"
        )

    return email


def get_user(self, username: str):
    user = self.db.query(User).filter(User.username == username).first()
    if user:
        return user


def authenticate_user(self, username: str, password: str):
    user = self.db.query(User).filter(User.username == username).first()
    user = get_user(username)
    if not user:
        raise create_credentials_exception("Invalid username or password")
    if not verify_password(password, User.hashed_password):
        raise create_credentials_exception("Invalid password")
    return user


def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
    username = get_subject_for_token_type(token, "access")
    user = get_user(username=username)
    if user is None:
        raise create_credentials_exception("Could not find user for this token")
    return user


def get_current_active_user(
    current_user: Annotated[UserSchema, Depends(get_current_user)],
):
    if not current_user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user
