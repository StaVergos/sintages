from fastapi import FastAPI

from src.api.users.routes import router as users_router
from src.api.ingredients.routes import router as ingredients_router
from src.api.categories.routes import router as categories_router

app = FastAPI()


app.include_router(users_router, prefix="/users", tags=["users"])
app.include_router(ingredients_router, prefix="/ingredients", tags=["ingredients"])
app.include_router(categories_router, prefix="/categories", tags=["categories"])


@app.get("/health")
async def healthcheck():
    return {"status": "ok"}
