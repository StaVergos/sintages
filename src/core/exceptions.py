from src.core.enums import ErrorKind


class ErrorException(Exception):
    def __init__(
        self,
        code: int,
        message: str,
        kind: ErrorKind,
        source: str | None = None,
    ):
        self.code = code
        self.message = message
        self.kind = kind
        self.source = source
