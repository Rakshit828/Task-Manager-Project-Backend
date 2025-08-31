from .schemas import BookCreateSchema, BookUpdateSchema
from .models import Book

from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel import select, desc

class BookService:
    async def get_all_books(self, session: AsyncSession):
        statement = select(Book).order_by(desc(Book.created_at))
        result = await session.exec(statement)
        return result.all()


    async def get_a_book(self, book_uid: str, session: AsyncSession):
        statement = select(Book).where(Book.uuid == book_uid)
        result = await session.exec(statement)
        book = result.first()  #This will return the object/row itself
        return book  #This the dict form of the object/row


    async def create_book(self, book_data: BookCreateSchema, session: AsyncSession):
        book_create_dict = book_data.model_dump()
        book = Book(**book_create_dict)
        session.add(book)
        await session.commit()
        return book.model_dump()


    async def update_book(self, book_uid: str, update_data: BookUpdateSchema, session: AsyncSession):
        real_book_data = await self.get_a_book(book_uid, session)

        if real_book_data is not None:
            to_update_data = update_data.model_dump()
            for key, value in to_update_data.items():
                setattr(real_book_data, key, value)
                #The real row is updated here already, so we only have to do session.commit()

            await session.commit()
            return real_book_data
        else:
            return False


    async def delete_book(self, book_uid: str, session: AsyncSession):
        book_data_to_delete = await self.get_a_book(book_uid, session)
        if book_data_to_delete is not None:
            await session.delete(book_data_to_delete)
            await session.commit()
            return book_data_to_delete
        else:
            return False

