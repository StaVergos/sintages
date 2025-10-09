from fastapi import FastAPI

from src.api.users.routes import router as users_router
from src.api.ingredients.routes import router as ingredients_router

app = FastAPI()


app.include_router(users_router, prefix="/users", tags=["users"])
app.include_router(ingredients_router, prefix="/ingredients", tags=["ingredients"])


@app.get("/health")
async def healthcheck():
    return {"status": "ok"}
