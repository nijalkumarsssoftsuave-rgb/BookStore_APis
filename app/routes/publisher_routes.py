from typing import List

from fastapi import APIRouter, Depends
from motor.motor_asyncio import AsyncIOMotorClient

<<<<<<< HEAD
from app.database import get_database
=======
from app.database import get_db
>>>>>>> f38e70b (Final Commit)
from app.models.pydantics.publisher_pydantics import PublisherResponse, PublisherCreate, PublisherUpdate
from app.services.publisher_service import PublisherService

publisher_routers = APIRouter(
    prefix="/publishers",
    tags=["publishers"],
)


@publisher_routers.get("/", response_model=List[PublisherResponse])
<<<<<<< HEAD
async def retrieve_publishers(db: AsyncIOMotorClient = Depends(get_database)):
=======
async def retrieve_publishers(db: AsyncIOMotorClient = Depends(get_db)):
>>>>>>> f38e70b (Final Commit)
    service = PublisherService(db)
    return await service.retrieve_publishers()


@publisher_routers.post("/", response_model=PublisherResponse)
<<<<<<< HEAD
async def create_publisher(publisher_request: PublisherCreate, db: AsyncIOMotorClient = Depends(get_database)):
=======
async def create_publisher(publisher_request: PublisherCreate, db: AsyncIOMotorClient = Depends(get_db)):
>>>>>>> f38e70b (Final Commit)
    service = PublisherService(db)
    return await service.create_publisher(publisher_request)


@publisher_routers.get("/{publisher_id}", response_model=PublisherResponse)
<<<<<<< HEAD
async def retrieve_publisher(publisher_id: str, db: AsyncIOMotorClient = Depends(get_database)):
=======
async def retrieve_publisher(publisher_id: str, db: AsyncIOMotorClient = Depends(get_db)):
>>>>>>> f38e70b (Final Commit)
    service = PublisherService(db)
    return await service.retrieve_publisher(publisher_id)


@publisher_routers.put("/{publisher_id}", response_model=PublisherResponse)
<<<<<<< HEAD
async def update_publisher(publisher_id: str, publisher: PublisherUpdate, db: AsyncIOMotorClient = Depends(get_database)):
=======
async def update_publisher(publisher_id: str, publisher: PublisherUpdate, db: AsyncIOMotorClient = Depends(get_db)):
>>>>>>> f38e70b (Final Commit)
    service = PublisherService(db)
    return await service.update_publisher(publisher_id, publisher)

