# import re
# from http import HTTPStatus
#
# from bson import ObjectId
# from motor.motor_asyncio import AsyncIOMotorClient
# from typing import List, Dict, Any
#
# from starlette.responses import JSONResponse
#
# from app.models.db.book_model import Book
# from app.models.db.category_model import Category
# from app.models.pydantics.base_pydantics import TokenPayload
# from app.models.pydantics.book_pydantics import (
#     BookCreate,
#     BookUpdate,
#     BookResponse,
#     BaseSchema, BookCreateResponse
# )
# from fastapi import HTTPException
#
# from app.models.pydantics.category_pydantics import CategoryResponse
#
# class BookService:
#     def __init__(self, db: AsyncIOMotorClient):
#         self.db = db
#         self.collection = self.db.books
#         self.category_collection = self.db.category
#         self.users_collection = self.db.users
#         self.publisher_collection = self.db.publishers
#         self.review_collection = self.db.reviews
#
#     # async def create_book(self, book: BookCreate, user: TokenPayload) -> BookResponse:
#     #     user_detail = await self.users_collection.find_one({"_id": ObjectId(user.id)})
#     #     if user_detail:
#     #         if 'admin' not in user_detail['role'] and 'author' not in user_detail['role']:
#     #             raise HTTPException(status_code=HTTPStatus.FORBIDDEN, detail='You are not allowed to create books')
#     #     book_dict = book.model_dump()
#     #     book_dict['category'] = await self.__get_category_detail(book.category)
#     #     book_dict['author'] = await self.__get_author(user.id)
#     #     book = Book(**book_dict)
#     #     inserted = await self.collection.insert_one(book.model_dump())
#     #     return await self.retrieve_book(str(inserted.inserted_id))
#
#     async def create_book(self, book: BookCreate, user: TokenPayload) -> BookResponse:
#         user_detail = await self.users_collection.find_one({"_id": ObjectId(user.id)})
#
#         if user_detail:
#             if 'admin' not in user_detail['role'] and 'author' not in user_detail['role']:
#                 raise HTTPException(status_code=HTTPStatus.FORBIDDEN, detail='You are not allowed to create books')
#
#         book_dict = book.model_dump()
#
#         # ✅ Always store author
#         book_dict['author'] = ObjectId(user.id)
#
#         # ✅ Store category as ID
#         book_dict['category'] = ObjectId(book.category)
#
#         book = Book(**book_dict)
#         inserted = await self.collection.insert_one(book.model_dump())
#
#         return await self.retrieve_book(str(inserted.inserted_id))
#
#     async def enrich_book_data(self, book: Dict[str, Any]) -> Dict[str, Any]:
#         book = self.__replace_id(book)
#
#         # ✅ Safe author handling
#         if 'author' in book and book['author'] is not None:
#             if isinstance(book['author'], dict):
#                 book['author'] = await self.__get_author(book['author']['id'])
#             else:
#                 book['author'] = await self.__get_author(book['author'])
#
#         # Category (same logic if needed)
#         if 'category' in book and book['category'] is not None:
#             if isinstance(book['category'], dict):
#                 book['category'] = await self.__get_category_detail(book['category']['id'])
#             else:
#                 book['category'] = await self.__get_category_detail(book['category'])
#
#         publisher = await self.__get_publisher(book['id'])
#         review = await self.__get_review_detail(book['id'])
#
#         book['average_rating'] = review['avg_rating']
#         book['total_reviews'] = review['total_reviews']
#
#         if publisher is not None:
#             book['publisher'] = publisher
#
#         return book
#
#     # async def enrich_book_data(self, book: Dict[str, Any]) -> Dict[str, Any]:
#     #     book = self.__replace_id(book)
#     #     book['author'] = await self.__get_author(book['author']['id'])
#     #     publisher = await self.__get_publisher(book['id'])
#     #     review = await self.__get_review_detail(book['id'])
#     #     book['average_rating'] = review['avg_rating']
#     #     book['total_reviews'] = review['total_reviews']
#     #     if publisher is not None:
#     #         book['publisher'] = publisher
#     #     return book
#
#     async def retrieve_books(self, published_category: str) -> List[BookResponse]:
#         query = {}
#         if published_category == 'Published':
#             query = {'is_published': True}
#         elif published_category == 'Non-Published':
#             query = {'is_published': False}
#         result = self.collection.find(query)
#         books = [
#             BookResponse(**await self.enrich_book_data(book))
#             async for book in result
#         ]
#         return books
#
#     async def retrieve_book(self, book_id: str) -> BookResponse:
#         book = await self.collection.find_one({'_id': ObjectId(book_id)})
#         enriched_book = await self.enrich_book_data(book)
#         return BookResponse(**enriched_book)
#
#     async def __get_author(self, author_id: str) -> BaseSchema:
#         author = await self.users_collection.find_one({'_id': ObjectId(author_id)})
#         if not author:
#             raise HTTPException(
#                 status_code=HTTPStatus.NOT_FOUND,
#                 detail='Author not found'
#             )
#         author = self.__replace_id(author)
#         return BaseSchema(**author)
#
#     async def update_book(self, book_id: str, book: BookUpdate, user: TokenPayload) -> BookResponse:
#         user_detail = await self.users_collection.find_one({"_id": ObjectId(user.id)})
#         if user_detail:
#             if 'admin' or 'author' not in user_detail['role']:
#                 raise HTTPException(status_code=HTTPStatus.FORBIDDEN, detail='You are not allowed to update books')
#         if not await self.collection.find_one({'_id': ObjectId(book_id)}):
#             raise HTTPException(status_code=404, detail='Book not found.')
#         book_dict = book.dict(exclude_unset=True)
#         book_detail = await self.retrieve_book(book_id)
#         if book is not None and book_detail.author.id != user.id:
#             raise HTTPException(status_code=HTTPStatus.FORBIDDEN,
#                                 detail='You do not have permission to perform this operation.')
#         await self.collection.update_one({'_id': ObjectId(book_id)}, {'$set': book_dict})
#         return await self.retrieve_book(book_id)
#
#     async def delete_book(self, book_id: str, user: TokenPayload) -> None:
#         book = await self.collection.find_one({'_id': ObjectId(book_id)})
#         if not book:
#             raise HTTPException(status_code=404, detail='Book not found.')
#         if book['author']['id'] != user.id:
#             raise HTTPException(status_code=HTTPStatus.FORBIDDEN,
#                                 detail='You do not have permission to perform this operation.')
#         await self.collection.delete_one({'_id': ObjectId(book_id)})
#
#     async def __get_publisher(self, book_id: str):
#         publisher = await self.publisher_collection.find_one({'books': book_id})
#         if not publisher:
#             return None
#         publisher = self.__replace_id(publisher)
#         return publisher
#
#     async def __get_category_detail(self, category) -> CategoryResponse:
#         if re.fullmatch(r"[a-f0-9]{24}", category):
#             final_category = await self.category_collection.find_one({'_id': ObjectId(category)})
#             if final_category is None:
#                 raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail='Invalid category id')
#         else:
#             final_category = await self.category_collection.find_one({'name': category})
#             if final_category is None:
#                 result = await self.__insert_category(category)
#                 final_category = await self.category_collection.find_one({'_id': result})
#         if final_category is None:
#             HTTPException(status_code=HTTPStatus.NOT_FOUND, detail='Invalid category')
#         category = self.__replace_id(final_category)
#         return CategoryResponse(**category)
#
#     async def __insert_category(self, category: str) -> str:
#         category = Category(name=category)
#         result = await self.category_collection.insert_one(category.dict())
#         return result.inserted_id
#
#     async def __get_review_detail(self, book_id: str) -> dict[str, int | float]:
#         total_reviews = 0
#         total_ratings = 0
#         review_cursor = self.review_collection.find({'book_id': book_id})
#
#         async for review in review_cursor:
#             rating = review['rating']
#             total_ratings += rating
#             total_reviews += 1
#
#         avg_rating = round(total_ratings / total_reviews, 2) if total_reviews > 0 else 0
#
#         return {
#             'avg_rating': avg_rating,
#             'total_reviews': total_reviews,
#         }
#
#     async def publish_book(self, book_id: str, user: TokenPayload) -> BookResponse:
#         user = await self.users_collection.find_one({'_id': ObjectId(user.id)})
#         if 'admin' not in user['role'] and 'publisher' not in user['role']:
#             raise HTTPException(status_code=HTTPStatus.FORBIDDEN,detail='You are not allowed to publish books')
#         book = await self.collection.find_one({'_id': ObjectId(book_id)})
#         if not book:
#             raise HTTPException(status_code=404, detail='Book not found.')
#         await self.collection.update_one({'_id': ObjectId(book_id)}, {'$set': {'is_published': True}})
#         book = await self.collection.find_one({'_id': ObjectId(book_id)})
#         enriched_book = await self.enrich_book_data(book)
#         return BookResponse(**enriched_book)
#
#
#     @staticmethod
#     def __replace_id(document):
#         document['id'] = str(document.pop('_id'))
#         return document

from typing import List, Dict, Any
from http import HTTPStatus
from fastapi import HTTPException
from bson import ObjectId
import re

from app.models.pydantics.book_pydantics import BookResponse, BookUpdate
from app.models.pydantics.category_pydantics import CategoryResponse
from app.models.db.book_model import Book
from app.models.pydantics.base_pydantics import BaseSchema
from app.utils.util import TokenPayload


class BookService:

    def __init__(self, db):
        self.collection = db.books
        self.users_collection = db.users
        self.category_collection = db.categories
        self.publisher_collection = db.publishers
        self.review_collection = db.reviews

    # ---------------- CREATE ----------------
    async def create_book(self, book, user: TokenPayload) -> BookResponse:
        user_detail = await self.users_collection.find_one({"_id": ObjectId(user.id)})

        if user_detail:
            if 'admin' not in user_detail['role'] and 'author' not in user_detail['role']:
                raise HTTPException(
                    status_code=HTTPStatus.FORBIDDEN,
                    detail='You are not allowed to create books'
                )

        book_dict = book.model_dump()

        # Resolve category
        book_dict['category'] = await self.__get_category_detail(book.category)

        # Store author as ObjectId in DB
        book_dict['author'] = ObjectId(user.id)

        book_obj = Book(**book_dict)
        inserted = await self.collection.insert_one(book_obj.model_dump())

        return await self.retrieve_book(str(inserted.inserted_id))

    # ---------------- READ ----------------
    async def retrieve_books(self, published_category: str) -> List[BookResponse]:
        query = {}
        if published_category == 'Published':
            query = {'is_published': True}
        elif published_category == 'Non-Published':
            query = {'is_published': False}

        result = self.collection.find(query)
        books = [
            BookResponse(**await self.enrich_book_data(book))
            async for book in result
        ]
        return books

    async def retrieve_book(self, book_id: str) -> BookResponse:
        book = await self.collection.find_one({'_id': ObjectId(book_id)})
        if not book:
            raise HTTPException(status_code=404, detail='Book not found')

        enriched_book = await self.enrich_book_data(book)
        return BookResponse(**enriched_book)

    # ---------------- UPDATE ----------------
    async def update_book(self, book_id: str, book: BookUpdate, user: TokenPayload) -> BookResponse:
        user_detail = await self.users_collection.find_one({"_id": ObjectId(user.id)})

        if user_detail:
            if 'admin' not in user_detail['role'] and 'author' not in user_detail['role']:
                raise HTTPException(
                    status_code=HTTPStatus.FORBIDDEN,
                    detail='You are not allowed to update books'
                )

        existing_book = await self.collection.find_one({'_id': ObjectId(book_id)})
        if not existing_book:
            raise HTTPException(status_code=404, detail='Book not found.')

        # Only author can modify their own book
        if 'author' not in existing_book or str(existing_book['author']) != user.id:
            raise HTTPException(
                status_code=HTTPStatus.FORBIDDEN,
                detail='You do not have permission to perform this operation.'
            )

        book_dict = book.model_dump(exclude_unset=True)
        await self.collection.update_one({'_id': ObjectId(book_id)}, {'$set': book_dict})

        return await self.retrieve_book(book_id)

    # ---------------- DELETE ----------------
    async def delete_book(self, book_id: str, user: TokenPayload) -> None:
        book = await self.collection.find_one({'_id': ObjectId(book_id)})
        if not book:
            raise HTTPException(status_code=404, detail='Book not found.')

        if 'author' not in book or str(book['author']) != user.id:
            raise HTTPException(
                status_code=HTTPStatus.FORBIDDEN,
                detail='You do not have permission to perform this operation.'
            )

        await self.collection.delete_one({'_id': ObjectId(book_id)})

    # ---------------- PUBLISH ----------------
    async def publish_book(self, book_id: str, user: TokenPayload) -> BookResponse:
        user_detail = await self.users_collection.find_one({'_id': ObjectId(user.id)})

        if 'admin' not in user_detail['role'] and 'publisher' not in user_detail['role']:
            raise HTTPException(
                status_code=HTTPStatus.FORBIDDEN,
                detail='You are not allowed to publish books'
            )

        book = await self.collection.find_one({'_id': ObjectId(book_id)})
        if not book:
            raise HTTPException(status_code=404, detail='Book not found.')

        await self.collection.update_one({'_id': ObjectId(book_id)}, {'$set': {'is_published': True}})
        book = await self.collection.find_one({'_id': ObjectId(book_id)})

        enriched_book = await self.enrich_book_data(book)
        return BookResponse(**enriched_book)

    # ---------------- ENRICH ----------------
    async def enrich_book_data(self, book: Dict[str, Any]) -> Dict[str, Any]:
        book = self.__replace_id(book)

        # Safely resolve author
        if 'author' in book:
            book['author'] = await self.__get_author(str(book['author']))
        else:
            book['author'] = None

        publisher = await self.__get_publisher(book['id'])
        review = await self.__get_review_detail(book['id'])

        book['average_rating'] = review['avg_rating']
        book['total_reviews'] = review['total_reviews']

        if publisher is not None:
            book['publisher'] = publisher

        return book

    # ---------------- HELPERS ----------------
    async def __get_author(self, author_id: str) -> BaseSchema:
        author = await self.users_collection.find_one({'_id': ObjectId(author_id)})
        if not author:
            raise HTTPException(
                status_code=HTTPStatus.NOT_FOUND,
                detail='Author not found'
            )

        author = self.__replace_id(author)
        return BaseSchema(**author)

    async def __get_publisher(self, book_id: str):
        publisher = await self.publisher_collection.find_one({'books': book_id})
        if not publisher:
            return None
        publisher = self.__replace_id(publisher)
        return publisher

    async def __get_category_detail(self, category) -> CategoryResponse:
        if re.fullmatch(r"[a-f0-9]{24}", category):
            final_category = await self.category_collection.find_one({'_id': ObjectId(category)})
            if final_category is None:
                raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail='Invalid category id')
        else:
            final_category = await self.category_collection.find_one({'name': category})
            if final_category is None:
                result = await self.__insert_category(category)
                final_category = await self.category_collection.find_one({'_id': result})

        if final_category is None:
            raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail='Invalid category')

        category = self.__replace_id(final_category)
        return CategoryResponse(**category)

    async def __insert_category(self, category: str) -> str:
        result = await self.category_collection.insert_one({'name': category})
        return result.inserted_id

    async def __get_review_detail(self, book_id: str) -> dict:
        total_reviews = 0
        total_ratings = 0

        review_cursor = self.review_collection.find({'book_id': book_id})
        async for review in review_cursor:
            rating = review['rating']
            total_ratings += rating
            total_reviews += 1

        avg_rating = round(total_ratings / total_reviews, 2) if total_reviews > 0 else 0

        return {
            'avg_rating': avg_rating,
            'total_reviews': total_reviews,
        }

    @staticmethod
    def __replace_id(document):
        document['id'] = str(document.pop('_id'))
        return document
