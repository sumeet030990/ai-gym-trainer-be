from fastapi import APIRouter, Depends
from app.controllers.user_controller import get_all_users
from core.security import is_user_authenticated


router = APIRouter(prefix="/users", tags=["Users"])

@router.get("/")
def get_users(auth_user=Depends(is_user_authenticated)):
    result =  get_all_users()
    return result