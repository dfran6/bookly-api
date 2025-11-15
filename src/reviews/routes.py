from typing import List
from fastapi import APIRouter, Depends
from src.errors import ReviewNotFound
from src.reviews.schema import ReviewCreateModel, ReviewModel, ReviewUpdateModel
from src.db.models import Review, User
from src.reviews.service import ReviewService
from src.db.main import get_session
from sqlmodel.ext.asyncio.session import AsyncSession
from src.auth.dependencies import RoleChecker, get_current_user



review_router = APIRouter()
review_service = ReviewService()
role_checker = Depends(RoleChecker(['admin','user']))

@review_router.post('/book/{book_uid}')
async def add_review_to_book(book_uid:str, review_data : ReviewCreateModel, current_user:User = Depends(get_current_user), session:AsyncSession= Depends(get_session)):
    new_review = await review_service.add_review_to_book(
       user_email=current_user.email,
       review_data = review_data,
       book_uid= book_uid,
       session =session,
    )
    
    return new_review
 
@review_router.get('/',response_model=List[Review], dependencies=[role_checker])
async def get_all_reviews(session:AsyncSession = Depends(get_session)):
   reviews =  await review_service.get_all_reviews(session)
   return reviews

@review_router.get('/{review_uid}', dependencies=[role_checker])
async def get_a_review(review_uid:str, session:AsyncSession = Depends(get_session)):
   review =  await review_service.get_review(review_uid, session)
   
   if review is not None:
      return review
   raise ReviewNotFound()

@review_router.patch('/update_review/{book_uid}/{review_uid}')
async def update_review(book_uid:str,review_uid:str, updated_review_data: ReviewUpdateModel, current_user: User = Depends(get_current_user), session:AsyncSession= Depends(get_session) ):
   updated_review = await review_service.update_review(book_uid,review_uid, updated_review_data, session)
   
   if updated_review is not None:
      return updated_review
   
   raise ReviewNotFound()

@review_router.delete('/{review_uid}', dependencies=[role_checker], description="Endpoint to delete a review")
async def delete_book_review(review_uid, session:AsyncSession = Depends(get_session)):
   review = await review_service.delete_review(review_uid, session)
   
   if review is None:
      raise ReviewNotFound()
   
   return {"message":"Review successfully deleted"}