from .base import BooklyBaseException

class EmailAlreadyExistsError(BooklyBaseException):
    """Raised when user tries to signup with the existing email"""
    pass

class InvalidEmailError(BooklyBaseException):
    """Raised when user enters invalid or not existing email during login in"""
    pass

class InvalidPasswordError(BooklyBaseException):
    """Raised when user enters the invalid password during login in"""
    pass

class InvalidTokenError(BooklyBaseException):
    """Raised when the user gives the invalid token"""
    pass

class AccessTokenError(BooklyBaseException):
    """Raised when the user gives the Refresh Token instead of Access Token"""
    pass

class RefreshTokenError(BooklyBaseException):
    """Raised when the user gives the Access Token instead of Refresh Token"""
    pass

class InsufficientPermissionError(BooklyBaseException):
    """Raised when the user does not have permissions to access a method"""
    pass

class RevokedTokenError(BooklyBaseException):
    """Raised when the user gives the revoked token"""
    pass

