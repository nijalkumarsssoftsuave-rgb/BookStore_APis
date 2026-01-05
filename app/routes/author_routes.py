from fastapi import (
    APIRouter,
    Depends,
    HTTPException
)
from typing import List
<<<<<<< HEAD
from app.models.pydantics.author_pydantucs import (
=======
from app.models.pydantics.author_pydantics import (
>>>>>>> f38e70b (Final Commit)
    AuthorResponse,
    CreateAuthor,
    UpdateAuthor
)
from motor.motor_asyncio import AsyncIOMotorClient
<<<<<<< HEAD
from app.database import get_database
=======
from app.database import get_db
>>>>>>> f38e70b (Final Commit)
from app.services.author_service import AuthorService

author_router = APIRouter(prefix="/authors", tags=['authors'])


@author_router.get('/', response_model=List[AuthorResponse])
<<<<<<< HEAD
async def retrieve_authors(db: AsyncIOMotorClient = Depends(get_database)):
=======
async def retrieve_authors(db: AsyncIOMotorClient = Depends(get_db)):
>>>>>>> f38e70b (Final Commit)
    service = AuthorService(db)
    return await service.retrieve_authors()


@author_router.post('/', response_model=AuthorResponse, status_code=201)
<<<<<<< HEAD
async def create_author(author: CreateAuthor, db: AsyncIOMotorClient = Depends(get_database)):
=======
async def create_author(author: CreateAuthor, db: AsyncIOMotorClient = Depends(get_db)):
>>>>>>> f38e70b (Final Commit)
    service = AuthorService(db)
    return await service.create_author(author)


@author_router.get('/{author_id}', response_model=AuthorResponse)
async def retrieve_author(
<<<<<<< HEAD
        author_id: str, db: AsyncIOMotorClient = Depends(get_database)
=======
        author_id: str, db: AsyncIOMotorClient = Depends(get_db)
>>>>>>> f38e70b (Final Commit)
):
    try:
        service = AuthorService(db)
        return await service.retrieve_author(author_id)
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))


@author_router.put('/{author_id}', response_model=AuthorResponse)
async def update_author(
<<<<<<< HEAD
        author_id: str, author: UpdateAuthor, db: AsyncIOMotorClient = Depends(get_database)
=======
        author_id: str, author: UpdateAuthor, db: AsyncIOMotorClient = Depends(get_db)
>>>>>>> f38e70b (Final Commit)
):
    try:
        service = AuthorService(db)
        return await service.update_author(author_id, author)
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))
