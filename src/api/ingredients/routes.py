from fastapi import APIRouter, Depends, HTTPException
from src.api.ingredients.schemas import CreateIngredientSchema, GetIngredientSchema
from src.api.ingredients.services import IngredientRepository
from src.api.ingredients.dependencies import get_ingredient_repository

router = APIRouter()


@router.get("/ingredients", response_model=list[GetIngredientSchema])
async def get_ingredients(
    ingredient_repository: IngredientRepository = Depends(get_ingredient_repository),
) -> list[GetIngredientSchema]:
    return ingredient_repository.get_all_ingredients()


@router.get("/ingredients/{ingredient_id}", response_model=GetIngredientSchema)
async def get_ingredient(
    ingredient_id: int,
    ingredient_repository: IngredientRepository = Depends(get_ingredient_repository),
):
    ingredient = ingredient_repository.get_ingredient_by_id(ingredient_id)
    if ingredient is None:
        raise HTTPException(status_code=404, detail="Ingredient not found")
    return ingredient


@router.post("/ingredients", response_model=GetIngredientSchema)
async def create_ingredient(
    ingredient: CreateIngredientSchema,
    ingredient_repository: IngredientRepository = Depends(get_ingredient_repository),
) -> GetIngredientSchema:
    return ingredient_repository.create_ingredient(ingredient)
