from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from contextlib import asynccontextmanager
from enum import Enum
import logging

from src.books.routes import book_router
from src.auth.routes import auth_router
from src.tasks.routes import task_router
from src.admin.routes import admin_router, admin_checker
from src.db.main import init_db

from src.exceptions.base import create_exception_handler, BooklyBaseException
from src.exceptions.book_errors import (
    BookNotFoundError,
    EmptyBookTableError
)
from src.exceptions.task_errors import (
    TaskNotFoundError,
    EmptyTasksError
)
from src.exceptions.auth_errors import (
    EmailAlreadyExistsError,
    InvalidEmailError,
    InvalidPasswordError,
    InvalidTokenError,
    AccessTokenError,
    RefreshTokenError,
    InsufficientPermissionError,
    RevokedTokenError
)
from src.auth.dependencies import RoleChecker

version = 'v1'

@asynccontextmanager
async def life_span(app: FastAPI):
    #Code to run at the startup
    await init_db()
    yield
    #Code to run at the shutdown


app = FastAPI(
    title="Bookly",
    description="A REST API for book review web service",
    version= version,
)

class Tags(str, Enum):
    books = "Books"
    auth = "Authentication"
    tasks = "Tasks"
    admin = "Admin Panel"


# Mapping of exception -> (status_code, error_type, resolution)
error_mapping = {
    EmailAlreadyExistsError: (409, "EmailAlreadyExistsError", "Use another email to sign up"),
    InvalidEmailError: (400, "InvalidEmailError", "Provide a valid email address"),
    InvalidPasswordError: (400, "InvalidPasswordError", "Ensure password meets security requirements"),
    InvalidTokenError: (401, "InvalidTokenError", "Provide a valid token"),
    AccessTokenError: (401, "AccessTokenError", "Request a new access token"),
    RefreshTokenError: (401, "RefreshTokenError", "Request a new refresh token"),
    InsufficientPermissionError: (403, "InsufficientPermissionError", "Ensure your account has the necessary permissions"),
    RevokedTokenError: (401, "RevokedTokenError", "Login again to obtain a new token"),
    BookNotFoundError: (404, "BookNotFoundError", "Verify the book ID exists"),
    EmptyBookTableError: (404, "EmptyBookTableError", "Add books to the database before querying"),
    TaskNotFoundError: (404, "TaskNotFoundError", "Verify the book ID exists"),
    EmptyTasksError: (404, "EmptyTasksError", "Add tasks first")
}

# Register all handlers
for exc_class, (status_code, error_type, resolution) in error_mapping.items():
    app.add_exception_handler(
        exc_class,
        create_exception_handler(
            status_code=status_code,
            initial_detail={
                "type": "Error",
                "error_type": error_type,
                "resolution": resolution
            }
        )
    )


# #Adding a error handler for Internal Server Error
# @app.exception_handler(500)
# async def handler_server_error(request: Request, exception: BooklyBaseException):
#     return JSONResponse(
#         content={
#             "type": "Error",
#             "error_type": "Internal Server Error",
#             "resolution": ""
#         }
#     )


app.include_router(task_router, prefix=f'/api/{version}/tasks', tags=[Tags.tasks])
app.include_router(auth_router, prefix=f'/api/{version}/auth', tags=[Tags.auth])
app.include_router(admin_router, prefix=f'/api/{version}/admin', tags=[Tags.admin], dependencies=[admin_checker])

# app.include_router(book_router, prefix=f"/api/{version}/books", tags=[Tags.books])