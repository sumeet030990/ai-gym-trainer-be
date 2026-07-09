import uuid

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from db.database import Base
from db.mixins import TimestampMixin, UUIDPrimaryKeyMixin

class GymEquipments(UUIDPrimaryKeyMixin, TimestampMixin, Base):
    __tablename__ = "gym_equipments"

    gym_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("gyms.id", ondelete="CASCADE"), nullable=False, index=True)
    equipment_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("equipments.id", ondelete="CASCADE"), nullable=False, index=True)
    is_active: Mapped[bool] = mapped_column(nullable=False, default=True)