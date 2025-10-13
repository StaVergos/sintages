from fastapi import Depends
from src.core.dependencies import get_db
from src.api.ingredients.services import IngredientRepository


def get_ingredient_repository(db=Depends(get_db)) -> IngredientRepository:
    return IngredientRepository(db)
