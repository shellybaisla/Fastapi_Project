from fastapi import Depends, Request, HTTPException, status
from app.core.config import settings
from fastapi.security import APIKeyHeader
from sqlalchemy.orm import Session
import jwt
from jwt.exceptions import InvalidTokenError
from app.models.user import UserModel
from app.core.database import get_db


## Token Send -
api_key_header = APIKeyHeader(name="Authorization", auto_error=False)


def is_authenticated(request: Request, token: str = Depends(api_key_header), db: Session = Depends(get_db)):
    try:
        token = request.headers.get("authorization")
        if not token:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token are unauthorized")

        token = token.split(" ")[-1]

        data = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        user_id = data.get("id")

        user = db.query(UserModel).filter(UserModel.id == user_id).first()
        if not user:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="user are unauthorized")

        return user
    except InvalidTokenError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token are unauthorized")