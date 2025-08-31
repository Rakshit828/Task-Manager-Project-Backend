from passlib.context import CryptContext
from datetime import datetime, timedelta
import jwt
import uuid
import logging
from src.config import Config


pwd_context = CryptContext(schemes=['bcrypt'])
ACCESS_TOKEN_EXPIRE = 3600      # Specify the token expiry time in seconds
REFRESH_TOKEN_EXPIRE = 2        # Specifying the refresh token expiry time in days


def generate_password_hash(password: str):
    hash = pwd_context.hash(password)
    return hash

def verify_password(password: str, hash: str) -> bool:
    is_verified = pwd_context.verify(password, hash)
    return is_verified


def create_jwt_token(user_data: dict , expiry: timedelta= None, refresh: bool= False) -> str:
    if not expiry:
        expiry = timedelta(seconds=ACCESS_TOKEN_EXPIRE) if refresh is False else timedelta(days=REFRESH_TOKEN_EXPIRE)
    payload = {
        'user':user_data,
        'exp': datetime.now() + expiry,
        'jti': str(uuid.uuid4()),
        'refresh' : refresh
    }

    token = jwt.encode(
        payload=payload,
        key= Config.JWT_SECRET,
        algorithm=Config.JWT_ALGORITHM
    )
    return token


def decode_token(token: str) -> dict:
    try:
        token_data = jwt.decode(
            jwt=token,
            key=Config.JWT_SECRET,
            algorithms=[Config.JWT_ALGORITHM]
        )
        return token_data
    
    except jwt.PyJWTError as jwte:
        logging.exception(jwte)
        return None

    except Exception as e:
        logging.exception(e)
        return None