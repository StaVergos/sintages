from fastapi import FastAPI, Depends, HTTPException
from src.db.postgresql import get_db
from src.db.models.users import User
from src.db.models.ingredients import Ingredient
from src.api.schemas import (
    GetUserSchema,
    CreateUserSchema,
    UpdateUserSchema,
    GetIngredientSchema,
    CreateIngredientSchema,
)
from src.core.security import hash_password


app = FastAPI()


@app.get("/health")
async def healthcheck():
    return {"status": "ok"}


@app.get("/users")
async def get_users(db=Depends(get_db)) -> list[GetUserSchema]:
    users = db.query(User).all()
    return [GetUserSchema.model_validate(user) for user in users]


@app.get("/users/{user_id}")
async def get_user(user_id: int, db=Depends(get_db)) -> GetUserSchema:
    user = db.query(User).filter(User.id == user_id).first()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return GetUserSchema.model_validate(user)


@app.post("/users")
async def create_user(user: CreateUserSchema, db=Depends(get_db)) -> GetUserSchema:
    existing_user = (
        db.query(User)
        .filter((User.username == user.username) | (User.email == user.email))
        .first()
    )

    if existing_user:
        raise HTTPException(status_code=409, detail="Username or email already exists")

    hashed_password = hash_password(user.password)
    new_user = User(
        username=user.username,
        email=user.email,
        full_name=user.full_name,
        is_active=user.is_active,
        hashed_password=hashed_password,
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return GetUserSchema.model_validate(new_user)


@app.put("/users/{user_id}")
async def update_user(
    user_id: int, user: UpdateUserSchema, db=Depends(get_db)
) -> GetUserSchema:
    existing_user = db.query(User).filter(User.id == user_id).first()
    if not existing_user:
        raise HTTPException(status_code=404, detail="User not found")

    if (
        user.username != existing_user.username
        and db.query(User).filter(User.username == user.username).first()
    ):
        raise HTTPException(status_code=409, detail="Username already exists")

    if (
        user.email != existing_user.email
        and db.query(User).filter(User.email == user.email).first()
    ):
        raise HTTPException(status_code=409, detail="Email already exists")

    existing_user.username = user.username
    existing_user.email = user.email
    existing_user.full_name = user.full_name
    existing_user.is_active = user.is_active

    db.commit()
    db.refresh(existing_user)
    return GetUserSchema.model_validate(existing_user)


@app.get("/ingredients")
async def get_ingredients(db=Depends(get_db)) -> list[GetIngredientSchema]:
    ingredients = db.query(Ingredient).all()
    return [GetIngredientSchema.model_validate(ing) for ing in ingredients]


@app.get("/ingredients/{ingredient_id}")
async def get_ingredient(ingredient_id: int, db=Depends(get_db)) -> GetIngredientSchema:
    ingredient = db.query(Ingredient).filter(Ingredient.ing_id == ingredient_id).first()
    if ingredient is None:
        raise HTTPException(status_code=404, detail="Ingredient not found")
    return GetIngredientSchema.model_validate(ingredient)


@app.post("/ingredients")
async def create_ingredient(
    ingredient: CreateIngredientSchema, db=Depends(get_db)
) -> GetIngredientSchema:
    existing_ingredient = (
        db.query(Ingredient)
        .filter((Ingredient.ing_name == ingredient.ing_name))
        .first()
    )

    if existing_ingredient:
        raise HTTPException(status_code=409, detail="Ingredient already exists")

    new_ingredient = Ingredient(
        ing_name=ingredient.ing_name,
        ing_amount=ingredient.ing_amount,
        ing_grams=ingredient.ing_grams,
        ing_category=ingredient.ing_category,
    )
    db.add(new_ingredient)
    db.commit()
    db.refresh(new_ingredient)
    return GetIngredientSchema.model_validate(new_ingredient)
