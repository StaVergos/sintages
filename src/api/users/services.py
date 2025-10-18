from fastapi import HTTPException, status
from src.api.users.schemas import CreateUserSchema, GetUserSchema
from src.db.models.users import User
from src.core.security import hash_password
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from src.core.exceptions import ErrorException
from src.core.enums import ErrorKind


class UserRepository:
    def __init__(self, db: Session):
        self.db = db

    @property
    def repo_name(self) -> str:
        return "UserRepository"

    def get_all_users(self) -> list[GetUserSchema]:
        users = self.db.query(User).all()
        return [GetUserSchema.model_validate(user) for user in users]

    def get_user_by_id(self, user_id: int) -> GetUserSchema | None:
        user = self.db.query(User).filter(User.id == user_id).first()
        if user:
            return GetUserSchema.model_validate(user)
        else:
            raise ErrorException(
                code=status.HTTP_404_NOT_FOUND,
                message="User not found",
                kind=ErrorKind.NOT_FOUND,
                source=f"{self.repo_name}.get_user_by_id",
            )

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

    def add_user(self, user: User) -> GetUserSchema:
        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)
        return GetUserSchema.model_validate(user)

    def create_user(self, user_data: CreateUserSchema) -> GetUserSchema:
        try:
            hashed_password = hash_password(user_data.password)
            new_user = User(
                username=user_data.username,
                email=user_data.email,
                full_name=user_data.full_name,
                is_active=user_data.is_active,
                hashed_password=hashed_password,
            )
            return self.add_user(new_user)
        except IntegrityError:
            raise ErrorException(
                code=status.HTTP_409_CONFLICT,
                message="Username or email already exists",
                kind=ErrorKind.CONFLICT,
                source=f"{self.repo_name}.create_user",
            )
        except Exception:
            raise ErrorException(
                code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                message="Internal server error",
                kind=ErrorKind.INTERNAL,
                source=f"{self.repo_name}.create_user",
            )

    def update_user(self, user_id: int, user_data: CreateUserSchema) -> GetUserSchema:
        user = self.db.query(User).filter(User.id == user_id).first()
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        try:
            user.username = user_data.username
            user.email = user_data.email
            user.full_name = user_data.full_name
            user.is_active = user_data.is_active
            self.db.commit()
            self.db.refresh(user)
            return GetUserSchema.model_validate(user)
        except IntegrityError:
            raise ErrorException(
                code=status.HTTP_409_CONFLICT,
                message="Username or email already exists",
                kind=ErrorKind.CONFLICT,
                source=f"{self.repo_name}.update_user",
            )
