from sqlalchemy.orm import Mapped, mapped_column

from db.database import Base
from db.mixins import TimestampMixin, UUIDPrimaryKeyMixin

class GoalQuestions(UUIDPrimaryKeyMixin, TimestampMixin, Base):
    __tablename__ = "goal_questions"

    question: Mapped[str] = mapped_column(nullable=False)
    is_multiple_choice: Mapped[bool] = mapped_column(nullable=False, default=False)
    is_active: Mapped[bool] = mapped_column(nullable=False, default=True)
    category: Mapped[int | None] = mapped_column(nullable=True)
    sort_order: Mapped[int | None] = mapped_column(nullable=True)