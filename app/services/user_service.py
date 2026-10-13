from fastapi import HTTPException,status,Request,Depends
from fastapi.security import APIKeyHeader
from app.schemas.user import UserSchema,LoginSchema
from sqlalchemy.orm import Session
from app.models.user import UserModel
from app.core.config import settings
from datetime import datetime,timedelta
from pwdlib import PasswordHash
from app.core.database import get_db


import jwt
from jwt.exceptions import InvalidTokenError

password_hash = PasswordHash.recommended()

def get_password_hash(password):
    return password_hash.hash(password) 

def verify_password(plain_password,hashed_password):
    return password_hash.verify(plain_password,hashed_password)

def register(body:UserSchema,db:Session):
    ## 1. Username Validation
    is_user = db.query(UserModel).filter(UserModel.username == body.username).first()
    if is_user:
        raise HTTPException(400,detail="Username already exist..")

    ## 2. Email Validation
    is_user = db.query(UserModel).filter(UserModel.email == body.email).first()
    if is_user:
        raise HTTPException(400,detail="Email Address already exist..")

    hash_password = get_password_hash(body.password)

    new_user = UserModel(
        name = body.name,
        username = body.username,
        hash_password = hash_password,
        email = body.email
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user


def login_user(body:LoginSchema,db:Session):
    user = db.query(UserModel).filter(UserModel.username == body.username).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Invalid username or password")

    if not verify_password(body.password,user.hash_password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Invalid username or password")

    exp_time = datetime.now() + timedelta(minutes=30)
    print(exp_time)
    token = jwt.encode({"id": user.id,"exp":exp_time.timestamp()},settings.SECRET_KEY,settings.ALGORITHM)

    return {"token":token}

api_key_header = APIKeyHeader(name="Authorization", auto_error=False)

## Token Send - 

api_key_header = APIKeyHeader(name="Authorization", auto_error=False)

def is_authenticated(
    request: Request,
    token: str = Depends(api_key_header),
    db: Session = Depends(get_db),
):
    try:
        token = request.headers.get("authorization")
        if not token:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token are unauthorized",
            )

        token = token.split(" ")[-1]

        data = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        user_id = data.get("id")

        user = db.query(UserModel).filter(UserModel.id == user_id).first()
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="user are unauthorized",
            )

        return user
    except InvalidTokenError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token are unauthorized",
        )

# def is_authenticated(request:Request,token: str = Depends(api_key_header),db:Session = Depends(get_db)):
#     try:
#         token = request.headers.get("authorization")
#         if not token:
#             raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Token are unauthorized")

#         token = token.split(" ")[-1]

#         data = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
#         user_id = data.get("id")
#         # exp_time = int(data.get("exp"))
#         # current_time = datetime.now().timestamp()

#         # if current_time > exp_time:
#         #     raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="you are unauthorized")

#         user = db.query(UserModel).filter(UserModel.id == user_id).first()
#         if not user:
#             raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="user are unauthorized")


#         return user
#     except InvalidTokenError:
#         raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Token are unauthorized")
