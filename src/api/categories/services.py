from fastapi import HTTPException
from src.db.models.categories import Category
from src.api.categories.schemas import (
    GetCategorySchema,
    CreateCategorySchema,
    UpdateCategorySchema,
)
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session


class CategoryRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_all_categories(self) -> list[GetCategorySchema]:
        categories = self.db.query(Category).all()
        return [GetCategorySchema.model_validate(cat) for cat in categories]

    def get_category_by_id(self, category_id: int) -> GetCategorySchema | None:
        category = self.db.query(Category).filter(Category.id == category_id).first()
        if category:
            return GetCategorySchema.model_validate(category)
        return None

    def add_category(self, category: Category) -> GetCategorySchema:
        self.db.add(category)
        self.db.commit()
        self.db.refresh(category)
        return GetCategorySchema.model_validate(category)

    def create_category(self, category_data: CreateCategorySchema) -> GetCategorySchema:
        try:
            new_category = Category(
                name=category_data.name,
                #                sub_name=category_data.sub_name,
            )
            return self.add_category(new_category)
        except IntegrityError:
            raise HTTPException(status_code=409, detail="Category already exists")

    def update_category(
        self, category_id: int, category_data: UpdateCategorySchema
    ) -> GetCategorySchema:
        category = self.db.query(Category).filter(Category.id == category_id).first()
        if not category:
            raise HTTPException(status_code=404, detail="Category not found")
        try:
            category.name = category_data.name
            #            category.sub_name = category_data.sub_name
            self.db.commit()
            self.db.refresh(category)
            return GetCategorySchema.model_validate(category)
        except IntegrityError:
            raise HTTPException(status_code=409, detail="Category already exists")
