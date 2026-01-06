from typing import List
from fastapi import APIRouter, HTTPException, Depends
from pydantic import EmailStr
from app.models.pydantics.base_pydantics import TokenResponse, TokenPayload
from app.utils.util import get_hashed_password
from app.models.pydantics.user_pydantics import (
    UserResponse,
    UserCreate,
    UserUpdate,
    UserLogin,
    ChangePasswordRequest
)
from motor.motor_asyncio import AsyncIOMotorClient
from app.services.user_service import UserService
from app.database import get_db
from app.utils.JWTToken import JWTBearer
from datetime import datetime, timedelta, timezone
from bson import ObjectId
import random
from fastapi import APIRouter
from app.models.pydantics.base_pydantics import TokenPayload
user_router = APIRouter(prefix="/users", tags=['Users'])

@user_router.post('/', response_model=TokenResponse)
async def create_user(user: UserCreate, db: AsyncIOMotorClient = Depends(get_db)):
    service = UserService(db)
    return await service.create_user(user)

@user_router.get('/', response_model=UserResponse)
async def get_user_details(
        user: TokenPayload = Depends(JWTBearer()),
        db: AsyncIOMotorClient = Depends(get_db)
):
    try:
        service = UserService(db)
        return await service.retrieve_user(user.id)
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@user_router.post('/login', response_model=TokenResponse)
async def login_user(user: UserLogin, db: AsyncIOMotorClient = Depends(get_db)):
    service = UserService(db)
    return await service.login_user(user)


@user_router.post('/change_password', status_code=201)
async def change_password(password_request: ChangePasswordRequest, db: AsyncIOMotorClient = Depends(get_db),
                          token: TokenPayload = Depends(JWTBearer())):
    service = UserService(db)
    return await service.change_user_password(password_request, token)


@user_router.post('/change_email', status_code=201)
async def change_email(new_email: EmailStr, db: AsyncIOMotorClient = Depends(get_db),
                       token: TokenPayload = Depends(JWTBearer())):
    service = UserService(db)
    return await service.change_email(new_email, token)


@user_router.post('/verify_otp', status_code=200)
async def verify_otp(otp: str, db: AsyncIOMotorClient = Depends(get_db),
                     token: TokenPayload = Depends(JWTBearer())):
    service = UserService(db)
    return await service.verify_otp(otp, token)
@user_router.put('/', response_model=UserResponse)
async def update_user(
        book: UserUpdate,
        user: TokenPayload = Depends(JWTBearer()),

        db: AsyncIOMotorClient = Depends(get_db)
):
    try:
        service = UserService(db)
        return await service.update_user(user.id, book)
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))

@user_router.put('/admin/update_user_role', status_code=201)
async def update_user_role(
        user_id: str,
        role: List[str],
        user: TokenPayload = Depends(JWTBearer()),

        db: AsyncIOMotorClient = Depends(get_db),
):
    try:
        service = UserService(db)
        return await service.update_user_role(user_id, role, user)
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))


@user_router.delete('/', status_code=204)
async def delete_user(
        user: TokenPayload = Depends(JWTBearer()),
        db: AsyncIOMotorClient = Depends(get_db)
):
    try:
        service = UserService(db)
        await service.delete_user(user.id)
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))


@user_router.delete('/admin/delete_user', status_code=204)
async def delete_user(
        user_id: str,
        user: TokenPayload = Depends(JWTBearer()),
        db: AsyncIOMotorClient = Depends(get_db)
):
    try:
        service = UserService(db)
        await service.delete_user_by_admin(user_id,user.id)
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))

@user_router.post("/generate-otp")
async def generate_otp(
    new_email: str,
    token: TokenPayload = Depends(JWTBearer()),
    db = Depends(get_db)
):
    collection = db["users"]

    user_db = await collection.find_one({"_id": ObjectId(token.id)})
    if not user_db:
        raise HTTPException(status_code=403, detail="Invalid user.")

    otp = str(random.randint(100000, 999999))

    hashed_otp = get_hashed_password(otp)

    otp_expiry = datetime.now(timezone.utc) + timedelta(minutes=5)

    await collection.update_one(
        {"_id": ObjectId(token.id)},
        {
            "$set": {
                "otp": hashed_otp,
                "otp_expires_at": otp_expiry,
                "temp_new_email": new_email
            }
        }
    )
    # Send OTP to new email
    await UserService.send_otp_email(new_email, otp)

    return {"message": "OTP sent successfully to your email."}
