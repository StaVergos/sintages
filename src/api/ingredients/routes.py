from fastapi import APIRouter, Depends
from src.api.ingredients.schemas import (
    CreateIngredientSchema,
    GetIngredientSchema,
    UpdateIngredientSchema,
)
from src.api.ingredients.services import IngredientRepository
from src.api.ingredients.dependencies import get_ingredient_repository
from src.core.schemas import ErrorResponse

router = APIRouter()

error_responses = {
    404: {"model": ErrorResponse, "description": "Ingredient not found"},
    409: {"model": ErrorResponse, "description": "Ingredient already exists"},
    422: {"model": ErrorResponse, "description": "Invalid Ingredient input format"},
    500: {"model": ErrorResponse, "description": "Internal server error"},
}


@router.get("/", response_model=list[GetIngredientSchema])
async def get_ingredients(
    ingredient_repository: IngredientRepository = Depends(get_ingredient_repository),
) -> list[GetIngredientSchema]:
    return ingredient_repository.get_all_ingredients()


@router.get("/{ingredient_id}", response_model=GetIngredientSchema)
async def get_ingredient(
    ingredient_id: int,
    ingredient_repository: IngredientRepository = Depends(get_ingredient_repository),
):
    ingredient = ingredient_repository.get_ingredient_by_id(ingredient_id)
    return ingredient


@router.post(
    "/", response_model=GetIngredientSchema, status_code=201, responses=error_responses
)
async def create_ingredient(
    ingredient: CreateIngredientSchema,
    ingredient_repository: IngredientRepository = Depends(get_ingredient_repository),
) -> GetIngredientSchema:
    return ingredient_repository.create_ingredient(ingredient)


@router.put(
    "/{ingredient_id}", response_model=GetIngredientSchema, responses=error_responses
)
async def update_ingredient(
    ingredient_id: int,
    ingredient: UpdateIngredientSchema,
    ingredient_repository: IngredientRepository = Depends(get_ingredient_repository),
) -> GetIngredientSchema:
    return ingredient_repository.update_ingredient(ingredient_id, ingredient)
