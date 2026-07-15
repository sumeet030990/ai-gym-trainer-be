import uuid
from datetime import date, datetime

from pydantic import BaseModel, ConfigDict, EmailStr, Field

_MOBILE_NO_PATTERN = r"^\+?[1-9]\d{7,14}$"


class UserRegisterRequest(BaseModel):
    """Request body for POST /register."""

    mobile_no: str = Field(pattern=_MOBILE_NO_PATTERN, description="E.164-style mobile number, e.g. +14155552671")
    # bcrypt only hashes the first 72 bytes of input; cap here so validation
    # fails clearly instead of bcrypt raising on truncation at hash time.
    password: str = Field(min_length=8, max_length=72)
    email: EmailStr | None = None
    first_name: str | None = Field(default=None, max_length=100)
    last_name: str | None = Field(default=None, max_length=100)
    birth_date: date | None = None
    role_id: uuid.UUID | None = Field(default=None, description="Optional role ID. If not provided, the default role will be assigned.")


class UserRegisterResponse(BaseModel):
    """Public representation of a newly registered user. Never includes the password/hash."""

    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    role_id: uuid.UUID
    mobile_no: str
    email: str | None
    first_name: str | None
    last_name: str | None
    birth_date: date | None
    created_at: datetime


class UserUpdateRequest(BaseModel):
    """Request body for PUT /users/{id}. Only fields explicitly provided are updated."""

    mobile_no: str | None = Field(default=None, pattern=_MOBILE_NO_PATTERN, description="E.164-style mobile number, e.g. +14155552671")
    email: EmailStr | None = None
    first_name: str | None = Field(default=None, max_length=100)
    last_name: str | None = Field(default=None, max_length=100)
    birth_date: date | None = None


class UserLoginRequest(BaseModel):
    """Request body for POST /login."""

    user_name: str
    password: str = Field(min_length=8, max_length=72)