import token

from fastapi import APIRouter,Depends,status,Request
from fastapi.security import APIKeyHeader
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.schemas.user import UserSchema,UserResponseSchema,LoginSchema
from app.services import user_service
from app.core.security import is_authenticated

user_routes = APIRouter(prefix="/users")


@user_routes.post("/register",response_model=UserResponseSchema,status_code=status.HTTP_201_CREATED)
def register(body:UserSchema,db:Session=Depends(get_db)):
    return user_service.register(body,db)

@user_routes.post("/Login",status_code=status.HTTP_200_OK)
def login(body:LoginSchema,db:Session=Depends(get_db)):
    return user_service.login_user(body,db)

api_key_header = APIKeyHeader(name="Authorization", auto_error=False)

# @user_routes.get("/is_auth",status_code=status.HTTP_200_OK,response_model=UserResponseSchema)
# def is_auth(request:Request,token: str = Depends(api_key_header),db:Session=Depends(get_db)):
#     return user_service.is_authenticated(request,db)

@user_routes.get("/is_auth", status_code=status.HTTP_200_OK, response_model=UserResponseSchema)
def is_auth(user=Depends(is_authenticated)):
    return user

