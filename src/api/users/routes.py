from fastapi import APIRouter, Depends
from src.api.users.schemas import CreateUserSchema, GetUserSchema, UpdateUserSchema
from src.api.users.services import UserRepository
from src.api.users.dependencies import get_user_repository
from src.core.schemas import ErrorResponse

router = APIRouter()

error_responses = {
    404: {"model": ErrorResponse, "description": "User not found"},
    409: {"model": ErrorResponse, "description": "User already exists"},
    422: {"model": ErrorResponse, "description": "Invalid user input format"},
    500: {"model": ErrorResponse, "description": "Internal server error"},
}


@router.get("/", response_model=list[GetUserSchema])
async def get_users(
    user_repository: UserRepository = Depends(get_user_repository),
) -> list[GetUserSchema]:
    return user_repository.get_all_users()


@router.get("/{user_id}", response_model=GetUserSchema)
async def get_user(
    user_id: int, user_repository: UserRepository = Depends(get_user_repository)
):
    user = user_repository.get_user_by_id(user_id)
    return user


@router.post(
    "/",
    response_model=GetUserSchema,
    status_code=201,
    responses=error_responses,
)
async def create_user(
    user: CreateUserSchema,
    user_repository: UserRepository = Depends(get_user_repository),
) -> GetUserSchema:
    return user_repository.create_user(user)


@router.put(
    "/{user_id}",
    response_model=GetUserSchema,
    responses=error_responses,
)
async def update_user(
    user_id: int,
    user: UpdateUserSchema,
    user_repository: UserRepository = Depends(get_user_repository),
) -> GetUserSchema:
    return user_repository.update_user(user_id, user)
