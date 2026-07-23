import uuid

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from db.database import Base
from db.mixins import TimestampMixin, UUIDPrimaryKeyMixin

class ExerciseVideos(UUIDPrimaryKeyMixin, TimestampMixin, Base):
    __tablename__ = "exercise_videos"

    excercise_id: Mapped[uuid.UUID | None] = mapped_column(ForeignKey("exercises.id", ondelete="CASCADE"), nullable=True, index=True)
    video_url: Mapped[str | None] = mapped_column(nullable=True)
    video_provider: Mapped[str | None] = mapped_column(nullable=True)