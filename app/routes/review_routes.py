from typing import List, Optional

from fastapi import APIRouter, Depends, Query, Path
from motor.motor_asyncio import AsyncIOMotorClient
from app.models.pydantics.base_pydantics import TokenPayload
from app.database import get_db
from app.services.review_service import ReviewService
from app.models.pydantics.review_pydantics import ReviewResponse, ReviewCreate, ReviewUpdate
from app.utils.JWTToken import JWTBearer

review_routers = APIRouter(
    prefix="/books",
    tags=['Reviews']
)


@review_routers.get(
    '/{book_id}/reviews',
    response_model=List[ReviewResponse]
)
async def retrieve_reviews(
        book_id: str,
        token: TokenPayload = Depends(JWTBearer()),
        db: AsyncIOMotorClient = Depends(get_db),
):
    service = ReviewService(db)
    return await service.retrieve_reviews(token, book_id)

# async def retrieve_reviews(
#         book_id: str,
#         user_id: str = Depends(JWTBearer()),
#
#         db: AsyncIOMotorClient = Depends(get_db),
# ):
#     service = ReviewService(db)
#     return await service.retrieve_reviews(user_id, book_id)


@review_routers.post(
    '/{book_id}/reviews',
    status_code=201,
    response_model=ReviewResponse
)
async def create_review(
    review: ReviewCreate,
    book_id: str,
    token: TokenPayload = Depends(JWTBearer()),   # <-- already decoded
    db: AsyncIOMotorClient = Depends(get_db)
):
    service = ReviewService(db)
    return await service.create_review(review, book_id, token)


@review_routers.get('/{book_id}/reviews/{review_id}',
                    response_model=ReviewResponse)
async def retrieve_review(
        review_id: str,
        book_id: str = None,
        db: AsyncIOMotorClient = Depends(get_db)
):
    service = ReviewService(db)
    return await service.retrieve_review(review_id)

# @review_routers.get('/{book_id}/reviews/{review_id}',
#                     response_model=ReviewResponse)
# async def retrieve_review(
#         review_id: str,
#         book_id: str,
#         db: AsyncIOMotorClient = Depends(get_db)
# ):
#     service = ReviewService(db)
#     return await service.retrieve_review(review_id, book_id)


@review_routers.put('/{book_id}/reviews/{review_id}', response_model=ReviewResponse)
async def update_review(
        review_id: str,
        review: ReviewUpdate,
        book_id: str = None,

        db: AsyncIOMotorClient = Depends(get_db)
):
    service = ReviewService(db)
    return await service.update_review(
        review_id,
        review,
    )
