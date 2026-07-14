from typing_extensions import Annotated
from sqlalchemy.ext.asyncio import AsyncSession
from app.services import user_service
from db.database import get_session
from fastapi import HTTPException
from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
import jwt
from datetime import datetime, timedelta, timezone
from uuid import UUID
from core.config import settings
from pwdlib import PasswordHash


password_hash = PasswordHash.recommended()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

def hash_password(plain_password: str) -> str:
    return password_hash.hash(plain_password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return password_hash.verify(plain_password, hashed_password)



def create_access_token(data: dict):
    try:
        to_encode = data.copy()
        expire = datetime.now(timezone.utc) + timedelta(minutes=settings.access_token_expire_minutes)
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, settings.secret_key, algorithm=settings.algorithm)
        return encoded_jwt
    except Exception as e:
        print("Error creating access token:", e)
        raise e
    

async def is_user_authenticated(token: Annotated[str, Depends(oauth2_scheme)], db_session: AsyncSession = Depends(get_session)):
    try:
        user = jwt.decode(token, settings.secret_key, algorithms=[settings.algorithm])
        if user is None:
            raise HTTPException(status_code=401, detail="Invalid token")
        else:
            user_name = user.get("mobile_no") or user.get("email")
            if user_name is None:
                raise HTTPException(status_code=401, detail="Invalid token: missing user identifier")
            
            user_data = await user_service.get_user_by_mobile_or_email(user_name, db_session)
            if user_data is None:
                raise HTTPException(status_code=401, detail="Invalid token")
            return user_data
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token has expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")




