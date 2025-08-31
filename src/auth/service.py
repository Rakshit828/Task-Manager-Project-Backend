from .models import User
from .schemas import UserCreateSchema
from .utils import verify_password, generate_password_hash

from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel import select
from pydantic import EmailStr


# We define all the database interactions with these services and other
class AuthService:
    async def get_user_by_email(self, email: EmailStr, session: AsyncSession):
        """Returns the entire row of the user"""
        statement = select(User).where(User.email == email)
        result = await session.exec(statement)
        return result.first()
    

    async def email_exists(self, email: EmailStr, session: AsyncSession):
        """Check if email is in the database or not"""
        user = await self.get_user_by_email(email, session)
        return True if user else False


    async def create_user(self, user_data: UserCreateSchema, session: AsyncSession):
        if user_data:
            user_data_dict = user_data.model_dump()
            new_user = User(**user_data_dict)
            new_user.password_hash = generate_password_hash(user_data_dict['password'])
            new_user.role = "user"
            session.add(new_user)
            await session.commit()
            return new_user
        return False
    

    async def login_user(self, password: str, password_hash: str):
        """Wrapper of verify password"""
        return verify_password(password, password_hash)
          
        
auth_service_provider = AuthService()