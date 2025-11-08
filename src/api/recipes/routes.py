from fastapi import APIRouter, Depends
from src.api.recipes.schemas import (
    CreateRecipeSchema,
    GetRecipeSchema,
    DeleteRecipeSchema,
)
from src.api.recipes.services import RecipeRepository
from src.api.recipes.dependencies import get_recipe_repository
from src.core.schemas import ErrorResponse

router = APIRouter()


@router.get(
    "/",
    response_model=list[GetRecipeSchema],
    responses={
        500: {"model": ErrorResponse, "description": "Internal server error"},
    },
)
async def get_recipes(
    recipe_repository: RecipeRepository = Depends(get_recipe_repository),
) -> list[GetRecipeSchema]:
    return recipe_repository.get_all_recipes()


@router.get(
    "/{recipe_id}",
    response_model=GetRecipeSchema,
    responses={
        404: {"model": ErrorResponse, "description": "Recipe not found"},
        500: {"model": ErrorResponse, "description": "Internal server error"},
    },
)
async def get_recipe(
    recipe_id: int,
    recipe_repository: RecipeRepository = Depends(get_recipe_repository),
):
    recipe = recipe_repository.get_recipe_by_id(recipe_id)
    return recipe


@router.get(
    "/{user_id}",
    response_model=GetRecipeSchema,
    responses={
        404: {"model": ErrorResponse, "description": "Recipe not found"},
        500: {"model": ErrorResponse, "description": "Internal server error"},
    },
)
async def get_recipes_user(
    user_id: int,
    recipe_repository: RecipeRepository = Depends(get_recipe_repository),
):
    recipe = recipe_repository.get_recipe_by_user(user_id)
    return recipe


@router.post(
    "/",
    response_model=GetRecipeSchema,
    status_code=201,
    responses={
        409: {"model": ErrorResponse, "description": "Recipe name already exists"},
        422: {"model": ErrorResponse, "description": "Invalid recipe input format"},
        500: {"model": ErrorResponse, "description": "Internal server error"},
    },
)
async def create_recipe(
    recipe: CreateRecipeSchema,
    recipe_repository: RecipeRepository = Depends(get_recipe_repository),
) -> GetRecipeSchema:
    return recipe_repository.create_recipe(recipe)


@router.delete(
    "/{recipe_id}",
    response_model=DeleteRecipeSchema,
    status_code=204,
    responses={
        404: {"model": ErrorResponse, "description": "Recipe not found"},
        500: {"model": ErrorResponse, "description": "Internal server error"},
    },
)
async def delete_recipe(
    recipe_id: int,
    recipe_repository: RecipeRepository = Depends(get_recipe_repository),
) -> DeleteRecipeSchema:
    return recipe_repository.delete_recipe_by_id(recipe_id)
