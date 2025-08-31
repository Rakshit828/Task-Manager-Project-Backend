from fastapi import APIRouter, HTTPException, status, Depends
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio.session import AsyncSession

from src.db.main import get_session
from src.db.redis import add_jti_to_blocklist
from .models import User
from .service import auth_service_provider
from .utils import create_jwt_token

from .schemas import (
    UserCreateSchema, 
    UserResponseSchema, 
    UserLoginSchema
)

from .dependencies import (
    RefreshTokenBearer, 
    AccessTokenBearer, 
    RoleChecker,
    get_current_user
)
from src.exceptions.auth_errors import (
    EmailAlreadyExistsError,
    InvalidEmailError,
    InvalidPasswordError,
)

auth_router = APIRouter()
admin_checker = Depends(RoleChecker(['admin']))


@auth_router.post(
    '/signup', 
    response_model=UserResponseSchema, 
    status_code=status.HTTP_201_CREATED,
)
async def create_user_account(user_data: UserCreateSchema, session: AsyncSession = Depends(get_session)):
    """Helps to register the account on the server"""
    email = user_data.email
    does_user_exists = await auth_service_provider.email_exists(email, session)
    if does_user_exists is True:
        raise EmailAlreadyExistsError()
    new_user = await auth_service_provider.create_user(user_data, session)
    return new_user



@auth_router.post(
    '/login',
    response_model=UserResponseSchema,
    status_code=status.HTTP_200_OK,
)
async def login_user(user_data: UserLoginSchema, session: AsyncSession = Depends(get_session)):
    """Verifies the credentials and issues both the Access Token and Refresh Token"""
    email = user_data.email
    password = user_data.password

    user = await auth_service_provider.get_user_by_email(email, session)
    if user:
        is_loggedin = await auth_service_provider.login_user(password, user.password_hash)
        if is_loggedin:
            access_token = create_jwt_token(
                user_data={"email": user.email, "user_uid": str(user.user_uid), "role": user.role}
            )
            refresh_token = create_jwt_token(
                user_data={"email": user.email, "user_uid": str(user.user_uid), "role": user.role},
                refresh=True
            )

            return JSONResponse(
                content={
                    "access_token": access_token, 
                    "refresh_token": refresh_token
                }, 
                status_code=status.HTTP_201_CREATED
            )
            
        raise InvalidPasswordError()
    raise InvalidEmailError()


# Use post request
@auth_router.get('/refresh', response_model=str)
async def create_new_access_tokens(
    refresh_token_details: dict = Depends(RefreshTokenBearer())
):
    access_token = create_jwt_token(
        user_data=refresh_token_details['user']
    )
    return JSONResponse(
        content={"access_token": access_token},
        status_code=status.HTTP_201_CREATED
    )


# Change this into a post request later
# We add the logic of automatically calling the /refresh when the token is expired
@auth_router.get('/logout')
async def revoke_token(token_details: dict = Depends(AccessTokenBearer())):
    jti = token_details['jti']
    await add_jti_to_blocklist(jti)
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={
            "message": "Logged Out Successfully !!!"
        }
    )


@auth_router.get('/me', dependencies=[admin_checker])
async def get_current_user(
    current_user: User = Depends(get_current_user),
):
    return current_user
