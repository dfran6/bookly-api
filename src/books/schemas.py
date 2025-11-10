from typing import List
from pydantic import BaseModel, Field
import uuid
from datetime import date, datetime
from src.reviews.schema import ReviewModel

class Book(BaseModel):
        uid: uuid.UUID
        title: str
        author: str
        year: date
        genre: str
        page_count: str
        created_at: datetime
        updated_at: datetime
        
class BookCreateModel(BaseModel):
        title: str
        author: str
        year: date
        genre: str
        page_count: str
        
class BookUpdateModel(BaseModel):
        title: str
        author: str
        genre: str
        page_count: str
        

class BookDetailModel(Book):
        reviews: List[ReviewModel]