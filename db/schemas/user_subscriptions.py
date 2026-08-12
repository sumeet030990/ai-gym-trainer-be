import enum
import uuid
from datetime import datetime, timezone
from typing import TYPE_CHECKING

from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey, func

from db.database import Base
from db.mixins import TimestampMixin, UUIDPrimaryKeyMixin
from db.schemas.subscription_plans import SubscriptionPlans

if TYPE_CHECKING:
    from db.schemas.users import Users

class SubscriptionStatus(enum.Enum):
    ACTIVE = "active"
    CANCELLED = "cancelled"
    EXPIRED = "expired"
    PAUSED = "paused"

class UserSubscriptions(UUIDPrimaryKeyMixin, TimestampMixin, Base):
    __tablename__ = "user_subscriptions"

    user_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("users.id"), nullable=False, index=True)
    subscription_plan_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("subscription_plans.id"), nullable=False, index=True)
    start_date: Mapped[datetime] = mapped_column(nullable=False, default=func.now())
    end_date: Mapped[datetime | None] = mapped_column(nullable=True)
    status: Mapped[SubscriptionStatus] = mapped_column(nullable=False, default=SubscriptionStatus.ACTIVE)

    user: Mapped["Users"] = relationship("Users", back_populates="subscriptions")
    subscription_plan: Mapped["SubscriptionPlans"] = relationship("SubscriptionPlans", foreign_keys=[subscription_plan_id])