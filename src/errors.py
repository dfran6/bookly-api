from typing import Any, Callable
from fastapi import FastAPI, status
from fastapi.requests import Request
from fastapi.responses import JSONResponse

class BooklyException(Exception):
    """
    this is the base class for all bookly errors 
    """
    

class InvalidToken(BooklyException):
    """
   User has provided an invalid or expired token
    """
    
class RevokedToken(BooklyException):
    """
   User has provided a token that has been revoked
    """
    
class AccessTokenRequired(BooklyException):
    """
   User has provided a referesh token when an access token is needed
    """

class RefreshTokenRequired(BooklyException):
    """
   User has provided a access token  when a  referesh token is needed
    """    
    
class UserAlreadyExists(BooklyException):
    """
   User has provided an email for a user who exits during sign up
    """
    
class InvalidCredentilas(BooklyException):
    """
   User has provided wrong an email or password during login
    """  
      
class InsufficientPermission(BooklyException):
    """
   User does not have the neccessary permissions to perform an action
    """    
    
class BookNotFound(BooklyException):
    """
   Book not found
    """    
    
class  ReviewNotFound(BooklyException):
    """
   Review not found
    """   
    
class TagNotFound(BooklyException):
    """
   Tag not found
    """    

    
class UserNotFound(BooklyException):
    """
   User not found
    """    
    
class AccountNotVerified(BooklyException):
    """
  User account not yet verified
    """    


def create_exception_handler(status_code:int, initial_detail:Any) -> Callable[[Request, Exception], JSONResponse]:
    
    async def exception_handler(request: Request, exc: BooklyException):
        
        return JSONResponse(
            content= initial_detail,
            status_code=status_code
        )
        
    return exception_handler


def register_all_errors(app:FastAPI):
    app.add_exception_handler(
        UserAlreadyExists,
        create_exception_handler(
            status_code=status.HTTP_403_FORBIDDEN,
            initial_detail= {
                "message": "User with email already exists",
                "error_code":"user_exists"
            }
        )
    )

    app.add_exception_handler(
        UserNotFound,
        create_exception_handler(
            status_code=status.HTTP_404_NOT_FOUND,
            initial_detail= {
                "message": "User not found",
                "error_code":"user_not_found"
            }
        )
    )
    app.add_exception_handler(
        BookNotFound,
        create_exception_handler(
            status_code=status.HTTP_404_NOT_FOUND,
            initial_detail= {
                "message": "Book not found",
                "error_code":"book_not_found"
            }
        )
    )
    app.add_exception_handler(
        ReviewNotFound,
        create_exception_handler(
            status_code=status.HTTP_404_NOT_FOUND,
            initial_detail= {
                "message": "Review not found",
                "error_code":"Review_not_found"
            }
        )
    )
    app.add_exception_handler(
        InvalidCredentilas,
        create_exception_handler(
            status_code=status.HTTP_400_BAD_REQUEST,
            initial_detail= {
                "message": "Invalid Email or Password",
                "error_code":"invalid_Email_or_password"
            }
        )
    )

    app.add_exception_handler(
        InvalidToken,
        create_exception_handler(
            status_code=status.HTTP_401_UNAUTHORIZED,
            initial_detail= {
                "message": "Token is invalid or expired",
                "resolution": "Please get a new token",
                "error_code":"invalid_token"
            }
        )
    )


    app.add_exception_handler(
        RevokedToken,
        create_exception_handler(
            status_code=status.HTTP_401_UNAUTHORIZED,
            initial_detail= {
                "message": "Token is invalid or has been revoked",
                "resolution": "Please get a new token",
                "error_code":"token_revoked"
            }
        )
    )

    app.add_exception_handler(
        AccessTokenRequired,
        create_exception_handler(
            status_code=status.HTTP_401_UNAUTHORIZED,
            initial_detail= {
                "message": "Please provide a valid access token",
                "resolution": "Please get a valid access token",
                "error_code":"access_token_required"
            }
        )
    )

    app.add_exception_handler(
        RefreshTokenRequired,
        create_exception_handler(
            status_code=status.HTTP_401_UNAUTHORIZED,
            initial_detail= {
                "message": "Please provide a valid refresh token",
                "resolution": "Please get a valid refresh token",
                "error_code":"refresh_token_required"
            }
        )
    )


    app.add_exception_handler(
        InsufficientPermission,
        create_exception_handler(
            status_code= status.HTTP_403_FORBIDDEN,
            initial_detail= {
                "message": "you are not allowed to perform this action",
                "resolution": "upgrade role",
                "error_code":"unauthorized_action"
            }
        )
    )
    
    app.add_exception_handler(
        AccountNotVerified,
         create_exception_handler(
            status_code= status.HTTP_403_FORBIDDEN,
            initial_detail= {
                "message": "account not verified",
                "resolution": "check email for verification details",
                "error_code":"account_not_verified"
            }
        )
        
    )

    @app.exception_handler(500)
    async def internal_server_error(request, exc):
            return JSONResponse(
                content={
                    "message":"Oops!.. something went wrong",
                    "error_code":"Server error",
                    
                },
                status_code= status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
        