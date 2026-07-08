import uuid

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from db.database import Base
from db.mixins import TimestampMixin, UUIDPrimaryKeyMixin


class UserConditions(UUIDPrimaryKeyMixin, TimestampMixin, Base):
    __tablename__ = "user_conditions"

    user_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    condition_name: Mapped[str] = mapped_column(nullable=False)
    notes: Mapped[str | None] = mapped_column(nullable=True)