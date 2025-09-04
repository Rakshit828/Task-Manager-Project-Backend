from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio.session import AsyncSession
from pydantic import EmailStr

# =====================================================
from src.auth.models import User
from src.auth.dependencies import RoleChecker
from src.auth.service import auth_service_provider
from src.db.main import get_session
from src.db.redis import add_jti_to_blocklist
from src.auth.schemas import UserCreateSchema, UserResponseSchema, UserLoginSchema
from .schemas import BanUserSchema

admin_router = APIRouter()
admin_checker = Depends(RoleChecker(['admin']))


@admin_router.post("/ban")
async def ban_a_user(
    user_data: BanUserSchema,  
    session: AsyncSession = Depends(get_session)
):
    pass


@admin_router.post("/unban")
async def unban_a_user(
    user_data: BanUserSchema,
    session: AsyncSession = Depends(get_session)
):
    pass

@admin_router.post('/getuser')
async def get_user_by_email(email: EmailStr, session: AsyncSession = Depends(get_session)):
    user_data = auth_service_provider.get_user_by_email(email, session)
    return user_data.model_dump()
