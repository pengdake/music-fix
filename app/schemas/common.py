from pydantic import BaseModel
from pydantic.generics import GenericModel
from typing import Generic, TypeVar

T = TypeVar('T')

class ResponseModel(GenericModel, Generic[T]):
    code: int
    message: str | None = None
    data: T | None = None

    @classmethod
    def success(cls, data: T, message: str | None = None):
        return cls(code=200, message=message, data=data)