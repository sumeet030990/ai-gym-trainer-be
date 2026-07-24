from fastapi import APIRouter
from routers.users import router as users_router
from routers.auth import router as auth_router
from routers.questions import router as questions_router
from routers.gym import router as gyms_router
api_router = APIRouter()

api_router.include_router(users_router)
api_router.include_router(auth_router)
api_router.include_router(questions_router) 
api_router.include_router(gyms_router)

@api_router.get("/")
def main():
    return {"message": "Hello World"}

