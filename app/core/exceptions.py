
class BaseException(Exception):
    """Base exception for the application."""
    def __int__(self, code: int, message: str, data: dict | None = None):
        self.code = code
        self.message = message
        self.data = data