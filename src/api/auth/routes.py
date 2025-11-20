from fastapi import APIRouter
from src.api.auth.services import authenticate_user, create_access_token
from src.api.auth.schemas import Token, LoginRequest


router = APIRouter()


@router.post("/token", response_model=Token)
async def login(user: LoginRequest) -> Token:
    user = authenticate_user(user.username, user.password)
    access_token = create_access_token(user.username)
    return Token(access_token=access_token, token_type="bearer")
