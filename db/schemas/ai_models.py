import uuid

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from db.database import Base
from db.mixins import TimestampMixin, UUIDPrimaryKeyMixin

class AiModels(UUIDPrimaryKeyMixin, TimestampMixin, Base):
    __tablename__ = "ai_models"

    name: Mapped[str] = mapped_column(nullable=False)
    ai_provider_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("ai_providers.id"), nullable=False, index=True)
    description: Mapped[str | None] = mapped_column(nullable=True)