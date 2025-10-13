from fastapi import Depends
from src.core.dependencies import get_db
from src.api.categories.services import CategoryRepository


def get_category_repository(db=Depends(get_db)) -> CategoryRepository:
    return CategoryRepository(db)
