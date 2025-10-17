from pydantic import BaseModel, Field

from src.core.enums import ErrorKind


class ErrorSchema(BaseModel):
    code: int = Field(ge=400, le=599, description="HTTP status code for the error")
    message: str = Field(max_length=255, description="Error message")
    kind: ErrorKind = Field("Type or category of the error")
    source: str | None = Field(
        max_length=100, description="Origin of the error (e.g., module or component)"
    )

    def as_exception_response(self) -> dict:
        return self.model_dump(exclude={"code"})
