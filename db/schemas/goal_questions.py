import enum
from typing import List, TYPE_CHECKING
import uuid

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from db.database import Base
from db.mixins import TimestampMixin, UUIDPrimaryKeyMixin
from db.schemas.goal_question_options import GoalQuestionOptions

if TYPE_CHECKING:
    from db.schemas.categories import Categories


class QUESTION_TYPE(enum.Enum):
    CHECKBOX = "checkbox"
    RADIO = "radio"
    TEXT = "text"

class GoalQuestions(UUIDPrimaryKeyMixin, TimestampMixin, Base):
    __tablename__ = "goal_questions"

    question: Mapped[str] = mapped_column(nullable=False)
    question_type: Mapped[QUESTION_TYPE] = mapped_column(nullable=False, default=QUESTION_TYPE.TEXT)
    is_active: Mapped[bool] = mapped_column(nullable=False, default=True)
    category_id: Mapped[uuid.UUID | None] = mapped_column(ForeignKey("categories.id", ondelete="SET NULL"), nullable=True, index=True)
    category: Mapped["Categories"] = relationship("Categories", back_populates="questions")
    sort_order: Mapped[int | None] = mapped_column(nullable=True)
    options: Mapped[List[GoalQuestionOptions]] = relationship(order_by="GoalQuestionOptions.sort_order")
