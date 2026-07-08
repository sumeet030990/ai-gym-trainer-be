import uuid

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from db.database import Base
from db.mixins import TimestampMixin, UUIDPrimaryKeyMixin

class GoalQuestionOptions(UUIDPrimaryKeyMixin, TimestampMixin, Base):
    __tablename__ = "goal_question_options"

    question_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("goal_questions.id"), nullable=False, index=True)
    label: Mapped[str] = mapped_column(nullable=False)
    sort_order: Mapped[int] = mapped_column(default=0)