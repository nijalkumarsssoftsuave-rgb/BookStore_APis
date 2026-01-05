from typing import List

from fastapi import APIRouter, Depends
from motor.motor_asyncio import AsyncIOMotorClient

<<<<<<< HEAD
from app.database import get_database
=======
from app.database import get_db
>>>>>>> f38e70b (Final Commit)
from app.models.pydantics.category_pydantics import CategoryCreate, CategoryResponse, CategoryUpdate
from app.services.category_service import CategoryService

category_router = APIRouter(prefix='/category', tags=['Category'])


@category_router.get('/', response_model=List[CategoryResponse])
<<<<<<< HEAD
async def retrieve_categories(db: AsyncIOMotorClient = Depends(get_database)):
=======
async def retrieve_categories(db: AsyncIOMotorClient = Depends(get_db)):
>>>>>>> f38e70b (Final Commit)
    service = CategoryService(db)
    return await service.retrieve_categories()


@category_router.post('/', response_model=CategoryResponse)
<<<<<<< HEAD
async def create_category(category: CategoryCreate, db: AsyncIOMotorClient = Depends(get_database)):
=======
async def create_category(category: CategoryCreate, db: AsyncIOMotorClient = Depends(get_db)):
>>>>>>> f38e70b (Final Commit)
    service = CategoryService(db)
    return await service.create_category(category)


@category_router.get('/{category_id}', response_model=CategoryResponse)
<<<<<<< HEAD
async def retrieve_category(category_id: str, db: AsyncIOMotorClient = Depends(get_database)):
=======
async def retrieve_category(category_id: str, db: AsyncIOMotorClient = Depends(get_db)):
>>>>>>> f38e70b (Final Commit)
    service = CategoryService(db)
    return await service.retrieve_category(category_id)


@category_router.put('/{category_id}', response_model=CategoryResponse)
<<<<<<< HEAD
async def update_category(category_id: str, category: CategoryUpdate, db: AsyncIOMotorClient = Depends(get_database)):
=======
async def update_category(category_id: str, category: CategoryUpdate, db: AsyncIOMotorClient = Depends(get_db)):
>>>>>>> f38e70b (Final Commit)
    service = CategoryService(db)
    return await service.update_category(category_id, category)
