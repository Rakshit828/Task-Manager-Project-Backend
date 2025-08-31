from typing import Callable, Any
from fastapi import Request
from fastapi.responses import JSONResponse


class BooklyBaseException(Exception):
    """A base class for all the client side exceptions"""
    pass


def create_exception_handler(
    status_code: int, 
    initial_detail: Any
) -> Callable[[Request, BooklyBaseException], JSONResponse]:

    async def exception_handler(request: Request, exception: BooklyBaseException):
        return JSONResponse(
            status_code=status_code,
            content=initial_detail
        )
    return exception_handler