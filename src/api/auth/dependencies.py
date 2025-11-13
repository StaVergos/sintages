from fastapi import Depends
from src.core.dependencies import get_db
from src.api.auth.services import AuthRepository


def auth_repository(db=Depends(get_db)) -> AuthRepository:
    return AuthRepository(db)
