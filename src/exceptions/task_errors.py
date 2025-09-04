from .base import BooklyBaseException

class TaskNotFoundError(BooklyBaseException):
    """Raised when the uuid of the task given by the user is invalid or not in the database"""
    pass

class EmptyTasksError(BooklyBaseException):
    """Raised when the user tries to access their task when it is empty"""
    pass
