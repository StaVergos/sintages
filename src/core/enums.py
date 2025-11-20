from enum import StrEnum


class ErrorKind(StrEnum):
    NOT_FOUND = "NotFoundError"
    INTERNAL = "InternalError"
    CONFLICT = "ConflictError"
    VALIDATION = "ValidationError"


class JWTType(StrEnum):
    ACCESS = "access"
    CONFIRMATION = "confirmation"
