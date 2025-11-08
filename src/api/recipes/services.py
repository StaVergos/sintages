from fastapi import status
from src.db.models.recipes import Recipe, RecipeIngredient
from src.db.models.ingredients import Ingredient
from src.db.models.users import User
from src.api.recipes.schemas import (
    GetRecipeSchema,
    CreateRecipeSchema,
    DeleteRecipeSchema,
    RecipeIngredientPayload,
)
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from src.core.exceptions import ErrorException
from src.core.enums import ErrorKind


class RecipeRepository:
    def __init__(self, db: Session):
        self.db = db

    @property
    def repo_name(self) -> str:
        return "RecipeRepository"

    def get_all_recipes(self) -> list[GetRecipeSchema]:
        recipes = self.db.query(Recipe).all()
        return [GetRecipeSchema.model_validate(recipe) for recipe in recipes]

    def get_recipe_by_id(self, recipe_id: int) -> GetRecipeSchema | None:
        recipe = self.db.query(Recipe).filter(Recipe.id == recipe_id).first()
        if recipe:
            return GetRecipeSchema.model_validate(recipe)
        else:
            raise ErrorException(
                code=status.HTTP_404_NOT_FOUND,
                message="Recipe not found",
                kind=ErrorKind.NOT_FOUND,
                source=f"{self.repo_name}.get_recipe_by_id",
            )

    def get_recipes_by_user(self, recipe_user_id: int) -> list[GetRecipeSchema]:
        recipes = self.db.query(Recipe).filter(Recipe.user_id == recipe_user_id).all()
        if recipes:
            return [GetRecipeSchema.model_validate(recipe) for recipe in recipes]
        raise ErrorException(
            code=status.HTTP_404_NOT_FOUND,
            message="Recipe not found for the user",
            kind=ErrorKind.NOT_FOUND,
            source=f"{self.repo_name}.get_recipes_by_user",
        )

    def add_recipe(self, recipe: Recipe) -> GetRecipeSchema:
        self.db.add(recipe)
        self.db.commit()
        self.db.refresh(recipe)
        return GetRecipeSchema.model_validate(recipe)

    def make_recipe_ingredients(
        self, items: list[RecipeIngredientPayload]
    ) -> list[RecipeIngredient]:
        if not items:
            return []

        ingredient_ids = [item.ingredient_id for item in items]

        ingredients = (
            self.db.query(Ingredient)
            .filter(Ingredient.id.in_(set(ingredient_ids)))
            .all()
        )
        ingredient_map = {ingredient.id: ingredient for ingredient in ingredients}
        missing_ids = [
            ing_id for ing_id in ingredient_ids if ing_id not in ingredient_map
        ]
        if missing_ids:
            raise ErrorException(
                code=status.HTTP_404_NOT_FOUND,
                message=f"Ingredients not found: {missing_ids}",
                kind=ErrorKind.NOT_FOUND,
                source=f"{self.repo_name}.make_recipe_ingredients",
            )
        return [
            RecipeIngredient(
                ingredient=ingredient_map[item.ingredient_id],
                quantity=item.quantity,
            )
            for item in items
        ]

    def create_recipe(self, recipe_data: CreateRecipeSchema) -> GetRecipeSchema:
        user = self.db.query(User).filter(User.id == recipe_data.user_id).first()
        if not user:
            raise ErrorException(
                code=status.HTTP_404_NOT_FOUND,
                message="User not found",
                kind=ErrorKind.NOT_FOUND,
                source=f"{self.repo_name}.create_recipe",
            )
        try:
            new_recipe = Recipe(
                name=recipe_data.name,
                cooking_time=recipe_data.cooking_time,
                difficulty_level=recipe_data.difficulty_level,
                portions=recipe_data.portions,
                instructions=recipe_data.instructions,
                user_id=recipe_data.user_id,
                user=user,
            )
            new_recipe.recipe_ingredients = self.make_recipe_ingredients(
                recipe_data.ingredients
            )
            return self.add_recipe(new_recipe)
        except IntegrityError:
            raise ErrorException(
                code=status.HTTP_409_CONFLICT,
                message="Recipe name already exists",
                kind=ErrorKind.CONFLICT,
                source=f"{self.repo_name}.create_recipe",
            )

    def delete_recipe_by_id(self, recipe_id: int) -> DeleteRecipeSchema:
        recipe = self.db.query(Recipe).filter(Recipe.id == recipe_id).first()
        if not recipe:
            raise ErrorException(
                code=status.HTTP_404_NOT_FOUND,
                message="Recipe not found",
                kind=ErrorKind.NOT_FOUND,
                source=f"{self.repo_name}.delete_recipe_by_id",
            )
        response = DeleteRecipeSchema.model_validate(recipe)
        self.db.delete(recipe)
        self.db.commit()
        return response
