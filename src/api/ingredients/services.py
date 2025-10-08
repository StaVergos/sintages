from fastapi import HTTPException
from src.db.models.ingredients import Ingredient
from src.api.ingredients.schemas import (
    GetIngredientSchema,
    CreateIngredientSchema,
)
from sqlalchemy.exc import IntegrityError


class IngredientRepository:
    def __init__(self, db):
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
                name=ingredient_data.name.lower(),
                is_vegan=ingredient_data.is_vegan,
            )
            return self.add_ingredient(new_ingredient)
        except IntegrityError:
            raise HTTPException(status_code=409, detail="Ingredient already exists")
