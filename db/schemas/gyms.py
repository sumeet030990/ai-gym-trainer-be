import uuid

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from db.database import Base
from db.mixins import TimestampMixin, UUIDPrimaryKeyMixin
from db.schemas.users import Users

class Gyms(UUIDPrimaryKeyMixin, TimestampMixin, Base):
    __tablename__ = "gyms"

    name: Mapped[str] = mapped_column(nullable=False)
    location: Mapped[str] = mapped_column(nullable=False)
    owner_user_id: Mapped[uuid.UUID | None] = mapped_column(ForeignKey("users.id", ondelete="SET NULL"), nullable=True, index=True)
    owner_data: Mapped[Users | None] = relationship("Users", foreign_keys=[owner_user_id])