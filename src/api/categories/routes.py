from fastapi import APIRouter, Depends, HTTPException
from src.api.categories.schemas import (
    CreateCategorySchema,
    GetCategorySchema,
    UpdateCategorySchema,
)
from src.api.categories.services import CategoryRepository
from src.api.categories.dependencies import get_category_repository

router = APIRouter()


@router.get("/", response_model=list[GetCategorySchema])
async def get_categories(
    category_repository: CategoryRepository = Depends(get_category_repository),
) -> list[GetCategorySchema]:
    return category_repository.get_all_categories()


@router.get("/{category_id}", response_model=GetCategorySchema)
async def get_category(
    category_id: int,
    category_repository: CategoryRepository = Depends(get_category_repository),
):
    category = category_repository.get_category_by_id(category_id)
    if category is None:
        raise HTTPException(status_code=404, detail="Category not found")
    return category


@router.post("/", response_model=GetCategorySchema)
async def create_category(
    category: CreateCategorySchema,
    category_repository: CategoryRepository = Depends(get_category_repository),
) -> GetCategorySchema:
    return category_repository.create_category(category)


@router.put("/{category_id}", response_model=GetCategorySchema)
async def update_category(
    category_id: int,
    category: UpdateCategorySchema,
    category_repository: CategoryRepository = Depends(get_category_repository),
) -> GetCategorySchema:
    return category_repository.update_category(category_id, category)
