from fastapi import FastAPI, status
from fastapi.responses import JSONResponse
from src.books.routes import book_router
from contextlib import asynccontextmanager
from src.db.main import init_db
from src.auth.routes import auth_router 
from src.reviews.routes import review_router
from src.errors import register_all_errors
from .middleware import register_middleware

@asynccontextmanager
async def life_span(app:FastAPI):
    print(f"server is starting....")
    await init_db()
    yield
    print(f"server has been stopped")

version ='v1'

app = FastAPI(
    title= 'Bookly',
    description='A REST API for a book review web server',
    version=version,
)

register_all_errors(app)

register_middleware(app)



app.include_router(book_router, prefix=f"/api/{version}/books", tags=['Books'])
app.include_router(auth_router, prefix=f"/api/{version}/users", tags=['Auth'])
app.include_router(review_router, prefix=f"/api/{version}/reviews", tags=['Reviews'])