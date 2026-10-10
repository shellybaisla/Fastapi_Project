import token

from fastapi import APIRouter,Depends,status,Request
from fastapi.security import APIKeyHeader
from sqlalchemy.orm import Session
from src.utils.db import get_db
from src.user.dtos import UserSchema,UserResponseSchema,LoginSchema
from src.user import controller

user_routes = APIRouter(prefix="/user")


@user_routes.post("/register",response_model=UserResponseSchema,status_code=status.HTTP_201_CREATED)
def register(body:UserSchema,db:Session=Depends(get_db)):
    return controller.register(body,db)

@user_routes.post("/Login",status_code=status.HTTP_200_OK)
def login(body:LoginSchema,db:Session=Depends(get_db)):
    return controller.login_user(body,db)

api_key_header = APIKeyHeader(name="Authorization", auto_error=False)

@user_routes.get("/is_auth",status_code=status.HTTP_200_OK,response_model=UserResponseSchema)
def is_auth(request:Request,token: str = Depends(api_key_header),db:Session=Depends(get_db)):
    return controller.is_authenticated(request,db)

