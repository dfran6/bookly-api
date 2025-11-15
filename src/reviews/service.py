from sqlmodel import desc, select
from src.errors import BookNotFound, UserNotFound
from src.reviews.schema import ReviewCreateModel, ReviewUpdateModel
from src.db.models import Review
from src.auth.service import UserService
from src.books.service import BookService
from sqlmodel.ext.asyncio.session import AsyncSession
from fastapi.exceptions import HTTPException
from fastapi import status, APIRouter, Depends
import logging


book_service = BookService()
user_service = UserService()


class ReviewService:
    
    async def add_review_to_book(self, user_email: str, book_uid:str,review_data:ReviewCreateModel, session: AsyncSession):
        try:
            book = await book_service.get_book(book_uid=book_uid, session=session)
            user = await user_service.get_user_by_email(user_email, session=session)
            review_data_dict = review_data.model_dump()
            
            new_review =Review(**review_data_dict)
            
            if not book:
                raise BookNotFound()
                
            if not user:
                raise UserNotFound()
                            
            new_review.user = user
            new_review.book = book
            
            session.add(new_review)
            await session.commit()
            
            return new_review
            
        except Exception as e:
            logging.exception(e)
            raise HTTPException(
                status_code= status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Oopps something went wrong"
            )
            
    async def get_review(self, review_uid:str, session:AsyncSession):
        statement = select(Review).where(Review.uid == review_uid)
        
        result =  await session.exec(statement)
        
        review = result.first()
        
        return review
        
            
    
    
    async def get_all_reviews(self, session: AsyncSession):
        statement = select(Review).order_by(desc(Review.created_at))
        
        result = await session.exec(statement)
        
        reviews = result.all()
        
        return reviews
    
    
    async def update_review(self, book_uid:str, review_uid:str, updated_review_data: ReviewUpdateModel, session:AsyncSession):
        statement = select(Review).where(Review.uid == review_uid and Review.book_uid == book_uid)
        
        result = await session.exec(statement)
        
        review_to_be_updated = result.first()
        
        if review_to_be_updated is not None:
            update_data_dict = updated_review_data.model_dump()
            
            for k,v in update_data_dict.items():
                setattr(review_to_be_updated, k, v)
                
            await session.commit()
            
            return review_to_be_updated
        
        else:
            return None
    
    
    async def delete_review(self, review_uid:str, session:AsyncSession):
        review_to_delete = await self.get_review( review_uid, session)
        
        if review_to_delete is not None:
            await session.delete(review_to_delete)
            
            await session.commit()
            
            return {}
        
        else:
            return None
        