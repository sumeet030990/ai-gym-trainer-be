import enum
import uuid

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from db.database import Base
from db.mixins import TimestampMixin, UUIDPrimaryKeyMixin


class LEVEL(enum.Enum):
    BEGINNER = "beginner"
    INTERMEDIATE = "intermediate"
    ADVANCED = "advanced"
class Exercises(UUIDPrimaryKeyMixin, TimestampMixin, Base):
    __tablename__ = "exercises"

    name: Mapped[str] = mapped_column(nullable=False)
    description: Mapped[str | None] = mapped_column(nullable=True)
    equipment_id: Mapped[uuid.UUID | None] = mapped_column(ForeignKey("gym_equipments.id", ondelete="CASCADE"), nullable=True, index=True)
    muscle_id: Mapped[uuid.UUID | None] = mapped_column(ForeignKey("muscles.id", ondelete="SET NULL"), nullable=True, index=True)
    excercise_level: Mapped[LEVEL | None] = mapped_column(nullable=False, default=LEVEL.BEGINNER)