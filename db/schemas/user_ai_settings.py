import uuid

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from db.database import Base
from db.mixins import TimestampMixin, UUIDPrimaryKeyMixin


class UserAiSettings(UUIDPrimaryKeyMixin, TimestampMixin, Base):
    __tablename__ = "user_ai_settings"

    user_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("users.id"), nullable=False, index=True)
    ai_provider_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("ai_providers.id"), nullable=False, index=True)
    ai_model_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("ai_models.id"), nullable=False, index=True)
    api_key: Mapped[str] = mapped_column(nullable=False)
    api_url: Mapped[str] = mapped_column(nullable=False)