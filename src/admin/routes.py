from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio.session import AsyncSession
from pydantic import EmailStr
from src.auth.models import User

# =====================================================
from auth.service import auth_service_provider
from db.main import get_session
from db.redis import add_jti_to_blocklist

admin_routes = APIRouter()

@admin_routes.post("/ban")
async def ban_a_user(email: EmailStr, session: AsyncSession = Depends(get_session)):
    pass

@admin_routes.post("/unban")
async def unban_a_user():
    pass

@admin_routes.post('/getuser')
async def get_user_by_email(email: EmailStr, session: AsyncSession = Depends(get_session)):
    user_data = auth_service_provider.get_user_by_email(email, session)
    return user_data.model_dump()
