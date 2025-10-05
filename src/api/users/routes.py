from fastapi import APIRouter, Depends, HTTPException
from src.api.users.schemas import CreateUserSchema, GetUserSchema, UpdateUserSchema
from src.api.users.services import UserRepository
from src.api.users.dependencies import get_user_repository

router = APIRouter()


@router.get("/users", response_model=list[GetUserSchema])
async def get_users(
    user_repository: UserRepository = Depends(get_user_repository),
) -> list[GetUserSchema]:
    return user_repository.get_all_users()


@router.get("/users/{user_id}", response_model=GetUserSchema)
async def get_user(
    user_id: int, user_repository: UserRepository = Depends(get_user_repository)
):
    user = user_repository.get_user_by_id(user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@router.post("/users", response_model=GetUserSchema)
async def create_user(
    user: CreateUserSchema,
    user_repository: UserRepository = Depends(get_user_repository),
) -> GetUserSchema:
    return user_repository.create_user(user)


@router.put("/users/{user_id}", response_model=GetUserSchema)
async def update_user(
    user_id: int,
    user: UpdateUserSchema,
    user_repository: UserRepository = Depends(get_user_repository),
) -> GetUserSchema:
    return user_repository.update_user(user_id, user)
