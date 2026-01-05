from fastapi import APIRouter, Depends
from motor.motor_asyncio import AsyncIOMotorClient
<<<<<<< HEAD
from app.database import get_database
=======
from app.database import get_db
>>>>>>> f38e70b (Final Commit)
from app.models.pydantics.search_pydantics import SearchByBooks, SearchByAuthors, SearchByCategories, SearchByReviews, \
    SearchByUsers
from app.services.search_service import SearchService

search_routers = APIRouter(
    prefix='/search',
    tags=['search'],
)


@search_routers.get(
    '/books',
    description='Search books by name, description, author or category',
    response_model=SearchByBooks,
)
<<<<<<< HEAD
async def search_books(input_str: str, db: AsyncIOMotorClient = Depends(get_database)):
=======
async def search_books(input_str: str, db: AsyncIOMotorClient = Depends(get_db)):
>>>>>>> f38e70b (Final Commit)
    service = SearchService(db)
    books = await service.search_books(input_str)
    return SearchByBooks(result=books)


@search_routers.get(
    '/authors',
    description=' Search authors by name, age, gender or awards.',
    response_model=SearchByAuthors,
)
<<<<<<< HEAD
async def search_author(input_str: str, db: AsyncIOMotorClient = Depends(get_database)):
=======
async def search_author(input_str: str, db: AsyncIOMotorClient = Depends(get_db)):
>>>>>>> f38e70b (Final Commit)
    service = SearchService(db)
    author = await service.search_author(input_str)
    return SearchByAuthors(result=author)


@search_routers.get(
    '/categories',
    description=' Search categories by name or description.',
    response_model=SearchByCategories,
)
<<<<<<< HEAD
async def search_category(input_str: str, db: AsyncIOMotorClient = Depends(get_database)):
=======
async def search_category(input_str: str, db: AsyncIOMotorClient = Depends(get_db)):
>>>>>>> f38e70b (Final Commit)
    service = SearchService(db)
    categories = await service.search_category(input_str)
    return SearchByCategories(result=categories)


@search_routers.get(
    '/reviews',
    description='Search reviews by content, rating, or user id.',
    response_model=SearchByReviews,
)
<<<<<<< HEAD
async def search_reviews(input_str: str, db: AsyncIOMotorClient = Depends(get_database)):
=======
async def search_reviews(input_str: str, db: AsyncIOMotorClient = Depends(get_db)):
>>>>>>> f38e70b (Final Commit)
    service = SearchService(db)
    reviews = await service.search_reviews(input_str)
    return SearchByReviews(result=reviews)


@search_routers.get(
    '/users',
    description='Search users by name, email, or phone number.',
    response_model=SearchByUsers,
)
<<<<<<< HEAD
async def search_user(input_str: str, db: AsyncIOMotorClient = Depends(get_database)):
=======
async def search_user(input_str: str, db: AsyncIOMotorClient = Depends(get_db)):
>>>>>>> f38e70b (Final Commit)
    service = SearchService(db)
    users = await service.search_user(input_str)
    return SearchByUsers(result=users)

