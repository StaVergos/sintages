from fastapi import HTTPException
from src.db.models.ingredients import Ingredient
from src.api.ingredients.schemas import (
    GetIngredientSchema,
    CreateIngredientSchema,
    UpdateIngredientSchema,
)
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session


class IngredientRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_all_ingredients(self) -> list[GetIngredientSchema]:
        ingredients = self.db.query(Ingredient).all()
        return [GetIngredientSchema.model_validate(ing) for ing in ingredients]

    def get_ingredient_by_id(self, ingredient_id: int) -> GetIngredientSchema | None:
        ingredient = (
            self.db.query(Ingredient).filter(Ingredient.id == ingredient_id).first()
        )
        if ingredient:
            return GetIngredientSchema.model_validate(ingredient)
        return None

    def add_ingredient(self, ingredient: Ingredient) -> GetIngredientSchema:
        self.db.add(ingredient)
        self.db.commit()
        self.db.refresh(ingredient)
        return GetIngredientSchema.model_validate(ingredient)

    def create_ingredient(
        self, ingredient_data: CreateIngredientSchema
    ) -> GetIngredientSchema:
        try:
            new_ingredient = Ingredient(
                name=ingredient_data.name,
                is_vegan=ingredient_data.is_vegan,
            )
            return self.add_ingredient(new_ingredient)
        except IntegrityError:
            raise HTTPException(status_code=409, detail="Ingredient already exists")

    def update_ingredient(
        self, ingredient_id: int, ingredient_data: CreateIngredientSchema
    ) -> GetIngredientSchema:
        ingredient = (
            self.db.query(Ingredient).filter(Ingredient.id == ingredient_id).first()
        )
        if not ingredient:
            raise HTTPException(status_code=404, detail="Ingredient not found")
        try:
            ingredient.name = ingredient_data.name
            ingredient.is_vegan = ingredient_data.is_vegan
            self.db.commit()
            self.db.refresh(ingredient)
            return GetIngredientSchema.model_validate(ingredient)
        except IntegrityError:
            raise HTTPException(status_code=409, detail="Ingredient already exists")
