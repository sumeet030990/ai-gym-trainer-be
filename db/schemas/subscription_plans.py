
import enum

from sqlalchemy.orm import Mapped, mapped_column

from db.database import Base

from db.mixins import TimestampMixin, UUIDPrimaryKeyMixin


class SubscriptionPlanFrequency(enum.Enum):
    MONTHLY = "monthly"
    QUARTERLY = "quarterly"
    YEARLY = "yearly"
    WEEKLY = "weekly"
    LIFETIME = "lifetime"
    
class SubscriptionPlans(UUIDPrimaryKeyMixin, TimestampMixin, Base):
    __tablename__ = "subscription_plans"
    
    name: Mapped[str] = mapped_column(nullable=False)
    price: Mapped[float] = mapped_column(nullable=False, default=0.0)
    currency: Mapped[str] = mapped_column(nullable=False, default="INR")
    frequency: Mapped[SubscriptionPlanFrequency] = mapped_column(nullable=False, default=SubscriptionPlanFrequency.MONTHLY)
    no_of_users: Mapped[int] = mapped_column(nullable=False, default=1)