from fastapi  import FastAPI
import uvicorn

from app.routes.category_routes import category_router
from app.routes.book_routes import book_router
from app.routes.author_routes import author_router
from app.routes.publisher_routes import publisher_routers
from app.routes.review_routes import review_routers
from app.routes.search_routes import search_routers
from app.routes.user_routes import user_router

app = FastAPI()

app.include_router(book_router)
app.include_router(author_router)
app.include_router(user_router)
app.include_router(review_routers)
app.include_router(category_router)
app.include_router(publisher_routers)
app.include_router(search_routers)


if __name__ == "__main__":
    uvicorn.run("app.main:app", host="192.168.5.207", port=5000, reload=True)

