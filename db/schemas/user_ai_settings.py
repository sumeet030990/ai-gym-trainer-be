
from datetime import datetime

from db.database import Base
import uuid

from sqlalchemy import ForeignKey, func
from sqlalchemy.orm import Mapped, mapped_column


class UserAiSettings(Base):
    __tablename__ = "user_ai_settings"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    user_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("users.id"), nullable=False)
    ai_provider_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("ai_providers.id"), nullable=False)
    ai_model_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("ai_models.id"), nullable=False)
    api_key: Mapped[str] = mapped_column(nullable=False)
    api_url: Mapped[str] = mapped_column(nullable=False)
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())