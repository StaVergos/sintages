from enum import StrEnum


class ErrorKind(StrEnum):
    NOT_FOUND = "NotFoundError"
    INTERNAL = "InternalError"
    CONFLICT = "ConflictError"
    VALIDATION = "ValidationError"


class TypeKind(StrEnum):
    access = "access"
    confirmation = "confirmation"
