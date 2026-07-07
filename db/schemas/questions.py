
from sqlalchemy.orm import Mapped, mapped_column
import uuid
from db.database import Base

class Questions(Base):
    __tablename__ = "questions"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    question: Mapped[str] = mapped_column(nullable=False)
    is_multiple_choice: Mapped[bool] = mapped_column(nullable=False, default=False)
    is_active: Mapped[bool] = mapped_column(nullable=False, default=True)
    category: Mapped[int] = mapped_column(nullable=True)
    sort_order: Mapped[int] = mapped_column(nullable=True)