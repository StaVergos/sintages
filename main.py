from fastapi import FastAPI, Depends, HTTPException

from src.db.postgresql import get_db
from src.db.models.ingredients import Ingredient
from src.api.schemas import (
    GetIngredientSchema,
    CreateIngredientSchema,
)

from src.api.users.routes import router as users_router


app = FastAPI()


app.include_router(users_router, prefix="/users", tags=["users"])


@app.get("/health")
async def healthcheck():
    return {"status": "ok"}


@app.get("/ingredients")
async def get_ingredients(db=Depends(get_db)) -> list[GetIngredientSchema]:
    ingredients = db.query(Ingredient).all()
    return [GetIngredientSchema.model_validate(ing) for ing in ingredients]


@app.get("/ingredients/{ingredient_id}")
async def get_ingredient(ingredient_id: int, db=Depends(get_db)) -> GetIngredientSchema:
    ingredient = db.query(Ingredient).filter(Ingredient.id == ingredient_id).first()
    if ingredient is None:
        raise HTTPException(status_code=404, detail="Ingredient not found")
    return GetIngredientSchema.model_validate(ingredient)


@app.post("/ingredients")
async def create_ingredient(
    ingredient: CreateIngredientSchema, db=Depends(get_db)
) -> GetIngredientSchema:
    existing_ingredient = (
        db.query(Ingredient).filter((Ingredient.name == ingredient.name)).first()
    )

    if existing_ingredient:
        raise HTTPException(status_code=409, detail="Ingredient already exists")

    new_ingredient = Ingredient(
        name=ingredient.name,
        is_vegan=ingredient.is_vegan,
    )
    db.add(new_ingredient)
    db.commit()
    db.refresh(new_ingredient)
    return GetIngredientSchema.model_validate(new_ingredient)
