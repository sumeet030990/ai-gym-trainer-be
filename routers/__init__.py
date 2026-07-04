from fastapi import APIRouter
from routers.users import router as users_router

api_router = APIRouter()

api_router.include_router(users_router)


@api_router.get("/")
def main():
    return {"message": "Hello World"}

