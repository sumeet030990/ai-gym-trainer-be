from datetime import date
import enum
import uuid

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from db.database import Base
from db.mixins import TimestampMixin, UUIDPrimaryKeyMixin
from db.schemas.roles import Roles
from db.schemas.user_ai_settings import UserAiSettings
from db.schemas.user_conditions import UserConditions
from db.schemas.user_goal_answer import UserGoalAnswers
from db.schemas.user_subscriptions import UserSubscriptions

class DietType(enum.Enum):
    VEGETARIAN = "vegetarian"
    EGGETARIAN = "eggetarian"
    NON_VEGETARIAN = "non_vegetarian"
    VEGAN = "vegan"
    PESCATARIAN = "pescatarian"
    KETO = "keto"
    LOW_CARB = "low_carb"
    MEDITERRANEAN = "mediterranean"
    OTHER = "other"

class UserSex(enum.Enum):
    MALE = "male"
    FEMALE = "female"
    OTHER = "other"
class Users(UUIDPrimaryKeyMixin, TimestampMixin, Base):
    __tablename__ = "users"

    role_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("roles.id"), nullable=False, index=True)
    email: Mapped[str | None] = mapped_column(unique=True, nullable=True)
    mobile_no: Mapped[str] = mapped_column(unique=True, nullable=False)
    password: Mapped[str] = mapped_column(nullable=False)
    first_name: Mapped[str | None] = mapped_column(nullable=True)
    last_name: Mapped[str | None] = mapped_column(nullable=True)
    birth_date: Mapped[date | None] = mapped_column(nullable=True)
    sex: Mapped[UserSex | None] = mapped_column(nullable=True)
    diet_type: Mapped[DietType] = mapped_column(default=DietType.VEGETARIAN)
    
    role: Mapped[Roles] = relationship("Roles", foreign_keys=[role_id])
    subscriptions: Mapped[list["UserSubscriptions"]] = relationship("UserSubscriptions", foreign_keys=[UserSubscriptions.user_id], cascade="all, delete-orphan")
    goals: Mapped[list["UserGoalAnswers"]] = relationship("UserGoalAnswers", foreign_keys=[UserGoalAnswers.user_id], cascade="all, delete-orphan")
    health_conditions: Mapped[list["UserConditions"]] = relationship("UserConditions", foreign_keys=[UserConditions.user_id], cascade="all, delete-orphan")
