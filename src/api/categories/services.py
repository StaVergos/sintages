from fastapi import HTTPException, status
from src.db.models.categories import Category
from src.api.categories.schemas import (
    GetCategorySchema,
    CreateCategorySchema,
    UpdateCategorySchema,
)
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from src.core.exceptions import ErrorException
from src.core.enums import ErrorKind


class CategoryRepository:
    def __init__(self, db: Session):
        self.db = db

    @property
    def repo_name(self) -> str:
        return "CategoryRepository"

    def get_all_categories(self) -> list[GetCategorySchema]:
        categories = self.db.query(Category).all()
        return [GetCategorySchema.model_validate(cat) for cat in categories]

    def get_category_by_id(self, category_id: int) -> GetCategorySchema | None:
        category = self.db.query(Category).filter(Category.id == category_id).first()
        if category:
            return GetCategorySchema.model_validate(category)
        else:
            raise ErrorException(
                code=status.HTTP_404_NOT_FOUND,
                message="Category not found",
                kind=ErrorKind.NOT_FOUND,
                source=f"{self.repo_name}.get_category_by_id",
            )

    def add_category(self, category: Category) -> GetCategorySchema:
        self.db.add(category)
        self.db.commit()
        self.db.refresh(category)
        return GetCategorySchema.model_validate(category)

    def create_category(self, category_data: CreateCategorySchema) -> GetCategorySchema:
        try:
            new_category = Category(
                name=category_data.name,
            )
            return self.add_category(new_category)
        except IntegrityError:
            raise ErrorException(
                code=status.HTTP_409_CONFLICT,
                message="Category name already exists",
                kind=ErrorKind.CONFLICT,
                source=f"{self.repo_name}.create_category",
            )
        except Exception:
            raise ErrorException(
                code=status.HTTP_500_ENTERNAL_SERVER_ERROR,
                message="Internal server error",
                kind=ErrorKind.INTERNAL,
                source=f"{self.repo_name}.create_category",
            )

    def update_category(
        self, category_id: int, category_data: UpdateCategorySchema
    ) -> GetCategorySchema:
        category = self.db.query(Category).filter(Category.id == category_id).first()
        if not category:
            raise HTTPException(status_code=404, detail="Category not found")
        try:
            category.name = category_data.name
            self.db.commit()
            self.db.refresh(category)
            return GetCategorySchema.model_validate(category)
        except IntegrityError:
            raise ErrorException(
                code=status.HTTP_409_CONFLICT,
                message="Category name already exists",
                kind=ErrorKind.CONFLICT,
                source=f"{self.repo_name}.update_category",
            )
