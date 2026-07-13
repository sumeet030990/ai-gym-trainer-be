from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.repositories import auth_repository
from app.schemas.auth_schemas import UserRegisterRequest, UserRegisterResponse
from core.security import hash_password, verify_password, create_access_token
from db.schemas import Users

DEFAULT_ROLE_NAME = "User"


async def register(payload: UserRegisterRequest, session: AsyncSession) -> Users:
    if await auth_repository.get_by_mobile_no(session, payload.mobile_no) is not None:
        raise HTTPException(status.HTTP_409_CONFLICT, "Mobile number is already registered.")

    if payload.email is not None and await auth_repository.get_by_email(session, payload.email) is not None:
        raise HTTPException(status.HTTP_409_CONFLICT, "Email is already registered.")

    role = await auth_repository.get_role_by_name(session, DEFAULT_ROLE_NAME)
    if role is None:
        raise HTTPException(
            status.HTTP_500_INTERNAL_SERVER_ERROR,
            f"Default role '{DEFAULT_ROLE_NAME}' is not configured.",
        )

    user = Users(
        role_id=role.id,
        mobile_no=payload.mobile_no,
        email=payload.email,
        password=hash_password(payload.password),
        first_name=payload.first_name,
        last_name=payload.last_name,
        birth_date=payload.birth_date,
    )
    return await auth_repository.create(session, user)



async def login(payload, session: AsyncSession):
    user = await auth_repository.get_by_mobile_or_email(session, payload.user_name)
    if user is None:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "Invalid credentials.")
    else:
        if not verify_password(payload.password, user.password):
            raise HTTPException(status.HTTP_401_UNAUTHORIZED, "Invalid credentials.")
        else:
            userData = UserRegisterResponse.model_validate(user).model_dump(mode="json")
            access_token = create_access_token(userData)
            return {"access_token": access_token, "user": userData}
    

    