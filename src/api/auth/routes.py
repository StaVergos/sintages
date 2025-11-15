from datetime import datetime, timedelta, timezone
from fastapi import Depends, APIRouter, HTTPException, status

from src.api.auth.services import AuthRepository
from src.api.auth.dependencies import auth_repository
from src.api.auth.schemas import Token, TokenData, LoginRequest
from src.core.config import config

router = APIRouter()


@router.post("/login", response_model=Token)
async def login_for_access_token(
    login_request: LoginRequest,
    auth_repository: AuthRepository = Depends(auth_repository),
) -> Token:
    user = auth_repository.authenticate_user(
        login_request.username, login_request.password
    )
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=config.ACCESS_TOKEN_EXPIRE_MINUTES)
    expiration_timestamp = datetime.now(timezone.utc) + access_token_expires

    data = TokenData(
        username=user.username,
        expiration_timestamp=expiration_timestamp.timestamp(),
    )
    access_token = auth_repository.create_access_token(token_data=data)
    return Token(access_token=access_token, token_type="bearer")
