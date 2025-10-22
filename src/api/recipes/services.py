from fastapi import status
from src.db.models.recipes import Recipe
from src.api.recipes.schemas import (
    GetRecipeSchema,
    CreateRecipeSchema,
    DeleteRecipeSchema,
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

    def get_recipe_by_user(self, recipe_user_id: int) -> GetRecipeSchema | None:
        recipe = self.db.query(Recipe).filter(Recipe.user_id == recipe_user_id).first()
        if recipe:
            return GetRecipeSchema.model_validate(recipe)
        else:
            raise ErrorException(
                code=status.HTTP_404_NOT_FOUND,
                message="Recipe not found for the user",
                kind=ErrorKind.NOT_FOUND,
                source=f"{self.repo_name}.get_recipe_by_user",
            )

    def add_recipe(self, recipe: Recipe) -> GetRecipeSchema:
        self.db.add(recipe)
        self.db.commit()
        self.db.refresh(recipe)
        return GetRecipeSchema.model_validate(recipe)

    def create_recipe(self, recipe_data: CreateRecipeSchema) -> GetRecipeSchema:
        try:
            new_recipe = Recipe(
                name=recipe_data.name,
                cooking_time=recipe_data.cooking_time,
                difficulty_level=recipe_data.difficulty_level,
                portions=recipe_data.portions,
                is_vegan=recipe_data.is_vegan,
                instructions=recipe_data.instructions,
                ingredients=recipe_data.ingredients,
                quantity=recipe_data.quantity,
                user_id=recipe_data.user_id,
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
        self.db.delete(recipe)
        self.db.commit()
        return DeleteRecipeSchema.model_validate(recipe)
