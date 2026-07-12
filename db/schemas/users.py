from datetime import date
import enum
import uuid

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from db.database import Base
from db.mixins import TimestampMixin, UUIDPrimaryKeyMixin

class DietType(enum.Enum):
    VEGETARIAN = "vegetarian"
    EGGETARIAN = "eggetarian"
    NON_VEGETARIAN = "non_vegetarian"
    
class Users(UUIDPrimaryKeyMixin, TimestampMixin, Base):
    __tablename__ = "users"

    role_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("roles.id"), nullable=False, index=True)
    email: Mapped[str | None] = mapped_column(unique=True, nullable=True)
    mobile_no: Mapped[str] = mapped_column(unique=True, nullable=False)
    password: Mapped[str] = mapped_column(nullable=False)
    first_name: Mapped[str | None] = mapped_column(nullable=True)
    last_name: Mapped[str | None] = mapped_column(nullable=True)
    birth_date: Mapped[date | None] = mapped_column(nullable=True)
    diet_type: Mapped[DietType] = mapped_column(default=DietType.NON_VEGETARIAN)
