from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from src.api.users.routes import router as users_router
from src.api.ingredients.routes import router as ingredients_router
from src.api.categories.routes import router as categories_router
from src.core.schemas import ErrorSchema
from src.core.exceptions import ErrorException

app = FastAPI()


@app.exception_handler(ErrorException)
async def exception_handler(request: Request, exc: ErrorException):
    error_response = ErrorSchema(
        code=exc.code,
        message=exc.message,
        kind=exc.kind,
        source=exc.source,
    )
    return JSONResponse(
        status_code=exc.code,
        content=error_response.as_exception_response(),
    )


app.include_router(users_router, prefix="/users", tags=["users"])
app.include_router(ingredients_router, prefix="/ingredients", tags=["ingredients"])
app.include_router(categories_router, prefix="/categories", tags=["categories"])


@app.get("/health")
async def healthcheck():
    return {"status": "ok"}
