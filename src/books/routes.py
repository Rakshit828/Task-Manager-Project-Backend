from fastapi import APIRouter, status, Depends
from sqlmodel.ext.asyncio.session import AsyncSession
from typing import List

from src.books.service import BookService
from src.books.schemas import BookResponseSchema, BookUpdateSchema, BookCreateSchema
from src.db.main import get_session
from src.auth.dependencies import AccessTokenBearer, RoleChecker

from src.exceptions.book_errors import (
    BookNotFoundError,
    EmptyBookTableError,
)


book_router = APIRouter()
book_service = BookService()

role_checker = Depends(RoleChecker(['admin', 'user']))
admin_checker = Depends(RoleChecker(['admin']))


@book_router.get(
    "/", 
    response_model=List[BookResponseSchema], 
    dependencies=[role_checker]
)
async def get_all_books(
    session: AsyncSession = Depends(get_session), 
    user_data: dict = Depends(AccessTokenBearer())  # We are actually calling the class to create the instance
):
    books =  await book_service.get_all_books(session)
    if books:
        return books
    raise EmptyBookTableError()



@book_router.post(
    "/", 
    status_code=status.HTTP_201_CREATED, 
    response_model=BookResponseSchema, 
    dependencies=[role_checker]
)
async def create_a_book(
    book_data: BookCreateSchema, 
    session: AsyncSession = Depends(get_session),
    user_data: dict = Depends(AccessTokenBearer())
):
    result = await book_service.create_book(book_data, session)
    return result 



@book_router.get(
    "/{book_id}", 
    response_model=BookResponseSchema, 
    dependencies=[role_checker]
)
async def get_book(
    book_uid: str, 
    session: AsyncSession = Depends(get_session),
    user_data: dict = Depends(AccessTokenBearer())
):
    result = await book_service.get_a_book(book_uid, session)
    if result:
        return result.model_dump()
    raise BookNotFoundError()


@book_router.patch(
    "/{book_id}", 
    response_model=BookResponseSchema, 
    dependencies=[role_checker]
)
async def update_book(
    book_uid: str, 
    book_data: BookUpdateSchema, 
    session: AsyncSession = Depends(get_session),
    user_data: dict = Depends(AccessTokenBearer())
):
    result = await book_service.update_book(book_uid=book_uid, update_data=book_data, session=session)
    if result:
        return result.model_dump()
    raise BookNotFoundError()



@book_router.delete(
    "/{book_id}", 
    response_model=BookResponseSchema, 
    dependencies=[role_checker]
)
async def delete_book(
    book_uid: str, 
    session: AsyncSession = Depends(get_session),
    user_data: dict = Depends(AccessTokenBearer())
):
    result = await book_service.delete_book(book_uid, session)
    if result:
        return result.model_dump()
    raise BookNotFoundError()

