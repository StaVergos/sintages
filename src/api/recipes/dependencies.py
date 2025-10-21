from fastapi import Depends
from src.core.dependencies import get_db
from src.api.recipes.services import RecipeRepository


def get_recipe_repository(db=Depends(get_db)) -> RecipeRepository:
    return RecipeRepository(db)
