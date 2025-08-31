from .base import BooklyBaseException


class BookNotFoundError(BooklyBaseException):
    """Raised when the user gives invalid book uuid"""
    pass

class EmptyBookTableError(BooklyBaseException):
    """Raised when the books table is empty and user tries to access them"""
    pass
