from fastapi import APIRouter
from app.Controllers.UserControllers import get_all_users

router = APIRouter(prefix="/users", tags=["Users"])

@router.get("/")
def get_users():
    result =  get_all_users()
    return result