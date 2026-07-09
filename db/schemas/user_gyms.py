import uuid

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from db.database import Base
from db.mixins import TimestampMixin, UUIDPrimaryKeyMixin


class UserGyms(UUIDPrimaryKeyMixin, TimestampMixin, Base):
    __tablename__ = "user_gyms"

    user_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    trainer_id: Mapped[uuid.UUID | None] = mapped_column(ForeignKey("users.id", ondelete="SET NULL"), nullable=True, index=True)
    gym_id: Mapped[uuid.UUID | None] = mapped_column(ForeignKey("gyms.id", ondelete="SET NULL"), nullable=True, index=True)