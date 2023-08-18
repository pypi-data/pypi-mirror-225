from typing import Generic, TypeVar, Optional
from pydantic import BaseModel

_T = TypeVar('_T')


class BaseApiOut(BaseModel, Generic[_T]):
    message: str = '请求成功'
    data: Optional[_T] = None
    code: int = 200


__all__ = [
    'BaseApiOut',
]
