import os
from typing import Annotated
from datetime import datetime, timedelta
from datetime import datetime, timedelta,timezone
from fastapi import Depends
from fastapi.security import HTTPBasicCredentials, HTTPBasic
from motor.motor_asyncio import AsyncIOMotorClient
from app.database import get_db
from app.models.pydantics.base_pydantics import TokenRequest, TokenPayload
from jose import jwt
from passlib.context import CryptContext

security = HTTPBasic()

ACCESS_TOKEN_EXPIRE_MINUTES = 30
REFRESH_TOKEN_EXPIRE_MINUTES = 60 * 24 * 30
ALGORITHM = "HS256"
JWT_SECRET_KEY = os.environ['JWT_SECRET_KEY']
JWT_REFRESH_SECRET_KEY = os.environ['JWT_REFRESH_SECRET_KEY']

password_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


from bcrypt import gensalt,checkpw,hashpw

def get_hashed_password(password: str) -> str:
    password_bytes = password.encode("utf-8")
    salt = gensalt()
    hashed = hashpw(password_bytes, salt)
    return hashed.decode("utf-8")   # store as string


def verify_password(password: str, hashed_pass: str) -> bool:
    password_bytes = password.encode('utf-8')
    hashed_bytes = hashed_pass.encode('utf-8')
    return checkpw(password_bytes, hashed_bytes)

def create_access_token(subject: TokenRequest) -> str:

    expires_delta = datetime.now(tz = timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

    to_encode = {"exp": expires_delta, "email": subject.email, "id": subject.id, "token_type": "access_token"}
    encoded_jwt = jwt.encode(to_encode, JWT_SECRET_KEY, ALGORITHM)
    # print(encoded_jwt)
    return encoded_jwt


def create_refresh_token(subject: TokenRequest) -> str:

    expires_delta = datetime.now(tz=timezone.utc) + timedelta(minutes=REFRESH_TOKEN_EXPIRE_MINUTES)

    to_encode = {"exp": expires_delta, "email": subject.email, "id": subject.id, "token_type": "refresh_token"}
    encoded_jwt = jwt.encode(to_encode, JWT_REFRESH_SECRET_KEY, ALGORITHM)
    return encoded_jwt


# def decode_jwt(token: str, is_refresh: bool) -> dict:
#     try:
#         if is_refresh:
#             key = JWT_REFRESH_SECRET_KEY
#         else:
#             key = JWT_SECRET_KEY
#         decoded_token = jwt.decode(token, key, algorithms=[ALGORITHM])
#         token_payload = TokenPayload(**decoded_token)
#         return decoded_token if datetime.fromtimestamp(token_payload.exp) >= datetime.now() else None
#
#     except Exception as e:
#         print(e)
#         return {}
#
# def decode_jwt(token: str, is_refresh: bool) -> dict:
#     try:
#         key = JWT_REFRESH_SECRET_KEY if is_refresh else JWT_SECRET_KEY
#
#         decoded_token = jwt.decode(token, key, algorithms=[ALGORITHM])
#         token_payload = TokenPayload(**decoded_token)
#
#         # exp is already a datetime
#         if token_payload.exp >= datetime.now(timezone.utc):
#             return decoded_token
#
#         return None
#
#     except Exception as e:
#         print("JWT ERROR:", e)
#         return {}


def decode_jwt(token: str, is_refresh: bool) -> dict:
    try:
        key = JWT_REFRESH_SECRET_KEY if is_refresh else JWT_SECRET_KEY

        decoded_token = jwt.decode(token, key, algorithms=[ALGORITHM])
        token_payload = TokenPayload(**decoded_token)

        exp_datetime = datetime.fromtimestamp(token_payload.exp, tz=timezone.utc)

        if exp_datetime >= datetime.now(timezone.utc):
            return decoded_token

        return None

    except Exception as e:
        print("JWT ERROR:", e)
        return {}


