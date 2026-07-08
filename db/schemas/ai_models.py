from db.database import Base
import uuid
from sqlalchemy import ForeignKey, func
from sqlalchemy.orm import Mapped, mapped_column
from datetime import datetime

class AiModels(Base):
    __tablename__ = "ai_models"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    name: Mapped[str] = mapped_column(nullable=False)
    ai_provider_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("ai_providers.id"), nullable=False)
    description: Mapped[str | None] = mapped_column(nullable=True)
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(server_default=func.now(), onupdate=func.now())