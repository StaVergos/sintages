from fastapi import Depends
from src.core.dependencies import get_db
from src.api.users.services import UserRepository


def get_user_repository(db=Depends(get_db)) -> UserRepository:
    return UserRepository(db)
