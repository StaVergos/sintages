from fastapi import HTTPException, status
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from src.db.models.ingredients import Ingredient
from src.db.models.categories import Category
from src.api.ingredients.schemas import (
    GetIngredientSchema,
    CreateIngredientSchema,
    UpdateIngredientSchema,
)
from src.api.common.schemas import CategoryRelationshipSchema
from src.core.exceptions import ErrorException
from src.core.enums import ErrorKind


class IngredientRepository:
    def __init__(self, db: Session):
        self.db = db

    @property
    def repo_name(self) -> str:
        return "IngredientRepository"

    def get_all_ingredients(self) -> list[GetIngredientSchema]:
        ingredients = self.db.query(Ingredient).all()
        return [GetIngredientSchema.model_validate(ing) for ing in ingredients]

    def get_ingredient_by_id(self, ingredient_id: int) -> GetIngredientSchema | None:
        ingredient = (
            self.db.query(Ingredient).filter(Ingredient.id == ingredient_id).first()
        )
        if ingredient:
            return GetIngredientSchema.model_validate(ingredient)
        else:
            raise ErrorException(
                code=status.HTTP_404_NOT_FOUND,
                message="Ingredient not found",
                kind=ErrorKind.NOT_FOUND,
                source=f"{self.repo_name}.get_ingredient_by_id",
            )

    def add_ingredient(self, ingredient: Ingredient) -> GetIngredientSchema:
        self.db.add(ingredient)
        self.db.commit()
        self.db.refresh(ingredient)
        return GetIngredientSchema.model_validate(ingredient)

    def get_categories(
        self, categories: list[CategoryRelationshipSchema]
    ) -> list[Category]:
        if not categories:
            return []
        categories_ids = [cat.id for cat in categories]
        categories = (
            self.db.query(Category).filter(Category.id.in_(categories_ids)).all()
        )
        return categories
        # exist_categories = {cat.id for cat in categories}
        # missing_ids = set(categories) - exist_categories
        # if missing_ids:
        #     raise ErrorException(
        #         code=status.HTTP_404_NOT_FOUND,
        #         message=f"Categories do not exist: {[cat.id for cat in missing_ids]}",
        #         kind=ErrorKind.NOT_FOUND,
        #         source=f"{self.repo_name}.get_categories",
        #     )

    def create_ingredient(
        self, ingredient_data: CreateIngredientSchema
    ) -> GetIngredientSchema:
        try:
            new_ingredient = Ingredient(
                name=ingredient_data.name,
                is_vegan=ingredient_data.is_vegan,
                categories=self.get_categories(ingredient_data.categories),
            )
            return self.add_ingredient(new_ingredient)
        except IntegrityError:
            raise ErrorException(
                code=status.HTTP_409_CONFLICT,
                message="Ingredient name already exists",
                kind=ErrorKind.CONFLICT,
                source=f"{self.repo_name}.create_ingredient",
            )

    def update_ingredient(
        self, ingredient_id: int, ingredient_data: UpdateIngredientSchema
    ) -> GetIngredientSchema:
        ingredient = (
            self.db.query(Ingredient).filter(Ingredient.id == ingredient_id).first()
        )
        if not ingredient:
            raise HTTPException(status_code=404, detail="Ingredient not found")
        try:
            if ingredient_data.name is not None:
                ingredient.name = ingredient_data.name
            if ingredient_data.is_vegan is not None:
                ingredient.is_vegan = ingredient_data.is_vegan
            if ingredient_data.categories is not None:
                ingredient.categories = self.get_categories(ingredient_data.categories)
            self.db.commit()
            self.db.refresh(ingredient)
            return GetIngredientSchema.model_validate(ingredient)
        except IntegrityError:
            raise ErrorException(
                code=status.HTTP_409_CONFLICT,
                message="Ingredient name already exists",
                kind=ErrorKind.CONFLICT,
                source=f"{self.repo_name}.update_ingredient",
            )
