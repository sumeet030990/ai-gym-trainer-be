from fastapi import APIRouter
from app.controllers.user_controller import get_all_users

router = APIRouter(prefix="/users", tags=["Users"])

@router.get("/")
def get_users():
    result =  get_all_users()
    return result