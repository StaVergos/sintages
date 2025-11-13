from datetime import datetime, timedelta
from typing import Annotated
from fastapi import Depends, APIRouter, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

from src.api.auth.services import AuthRepository
from src.api.auth.dependencies import auth_repository
from src.api.auth.schemas import Token
from src.core.config import config

router = APIRouter()


@router.post("/login", response_model=Token)
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    auth_repository: AuthRepository = Depends(auth_repository),
) -> Token:
    user = auth_repository.authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=config.ACCESS_TOKEN_EXPIRE_MINUTES)

    access_token = auth_repository.create_access_token(
        data={"sub": user.username},
        expiration_timestamp=datetime.utcnow(),
        expires_delta=access_token_expires,
    )
    return Token(access_token=access_token, token_type="bearer")
