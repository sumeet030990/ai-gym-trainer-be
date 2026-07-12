import uuid
from datetime import datetime

from sqlalchemy import func
from sqlalchemy.orm import Mapped, mapped_column


class UUIDPrimaryKeyMixin:
    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4, sort_order=-10)


class TimestampMixin:
    created_at: Mapped[datetime] = mapped_column(server_default=func.now(), sort_order=10)
    updated_at: Mapped[datetime] = mapped_column(server_default=func.now(), onupdate=func.now(), sort_order=10)
