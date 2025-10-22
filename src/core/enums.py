from enum import StrEnum


class ErrorKind(StrEnum):
    NOT_FOUND = "NotFoundError"
    INTERNAL = "InternalError"
    CONFLICT = "ConflictError"


class DifficultyLevel(StrEnum):
    EASY = "Easy"
    MEDIUM = "Medium"
    HARD = "Hard"
