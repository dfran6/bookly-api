from typing import List
import uuid
from pydantic import BaseModel, Field
from datetime import date, datetime
from src.books.schemas import BookCreateModel 
from src.reviews.schema import ReviewModel

class UserCreateModel(BaseModel):
    first_name: str = Field(max_length=25)
    last_name: str = Field(max_length=25)
    username: str = Field(max_length=8)
    email: str  = Field(max_length=40)
    password: str = Field(max_length=6)
    
    
class UserModel(BaseModel):
    uid: uuid.UUID 
    username: str
    email: str
    first_name: str
    last_name: str
    is_verified: bool
    password_hash: str = Field(exclude=True)
    created_at: datetime 
    updated_at: datetime
    
    
class UserBooksModel(UserModel):
    books: List[BookCreateModel]
    reviews:List[ReviewModel]
    
    
    
class UserLoginModel(BaseModel):
    email: str  = Field(max_length=40, min_length=2)
    password: str = Field(max_length=6)


class EmailModel(BaseModel):
    addresses:List[str]
    
    
class PasswordResetRequestModel(BaseModel):
    email:str
    
    
class PasswordResetConfirmModel(BaseModel):
    new_password: str
    confirm_new_password: str