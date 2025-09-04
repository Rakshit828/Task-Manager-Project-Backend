from fastapi.security import HTTPBearer
from fastapi import Depends, Request
from sqlmodel.ext.asyncio.session import AsyncSession
from typing import List

from .utils import decode_token
from .service import auth_service_provider
from .models import User
from src.db.redis import token_in_blocklist
from src.db.main import get_session

from src.exceptions.auth_errors import (
    InvalidTokenError,
    AccessTokenError, 
    RefreshTokenError,
    InsufficientPermissionError,
    RevokedTokenError,
)

class TokenBearer(HTTPBearer):
    def __init__(self, auto_error: bool = True):
        super().__init__(auto_error=auto_error)
    
    async def __call__(self, request: Request):
        scheme_and_credentials = await super().__call__(request)

        credentials = scheme_and_credentials.credentials
        token_data = decode_token(token=credentials)

        if not self.token_valid(token=credentials):
            raise InvalidTokenError() # Have to create a new token
    

        # Expired token will already fail at step 1. Redis is only to catch valid-but-revoked tokens
        # It is useful when the user logs out before the jwt access token expires
        # if await token_in_blocklist(token_data['jti']):
        #     raise HTTPException(
        #         status_code=status.HTTP_403_FORBIDDEN,
        #         detail={
        #             "Error": "The token is invalid or has been revoked",
        #             "resolution": "Create a new token"
        #         }
        #     )
        
        self.verify_token_data(token_data)
        return token_data
        

    def token_valid(self, token: str) -> True | False:
        token_data = decode_token(token=token)
        return (token_data is not None)


    def verify_token_data(self, token_data: str):
        raise NotImplementedError("Child Classes should implement this method.")
    


class AccessTokenBearer(TokenBearer):
     def verify_token_data(self, token_data: dict) -> None:
        if token_data and token_data["refresh"]:
            raise AccessTokenError()


class RefreshTokenBearer(TokenBearer):
    def verify_token_data(self, token_data: dict) -> None:
        if token_data and (not token_data["refresh"]):
            raise RefreshTokenError()



async def get_current_user(
    token_details: dict = Depends(AccessTokenBearer()),
    session: AsyncSession = Depends(get_session),
):
    user_email = token_details["user"]["email"]
    user = await auth_service_provider.get_user_by_email(user_email, session)
    return user



class RoleChecker:
    def __init__(self, allowed_roles: List[str]):
        self.allowed_roles = allowed_roles

    def __call__(self, current_user: User = Depends(get_current_user)):
        if current_user.role in self.allowed_roles:
            return True
        raise InsufficientPermissionError()