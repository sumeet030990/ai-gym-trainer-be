import uuid

from sqlalchemy import ForeignKey, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship
from db.schemas.goal_question_options import GoalQuestionOptions
from db.schemas.goal_questions import GoalQuestions
from db.database import Base
from db.mixins import TimestampMixin, UUIDPrimaryKeyMixin


class UserGoalAnswers(UUIDPrimaryKeyMixin, TimestampMixin, Base):
    __tablename__ = "user_goal_answers"
    __table_args__ = (
        UniqueConstraint("user_id", "question_id", "option_id", name="uq_user_goal_answers_user_question_option"),
    )

    user_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    question_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("goal_questions.id", ondelete="CASCADE"), nullable=False, index=True)
    option_id: Mapped[uuid.UUID | None] = mapped_column(ForeignKey("goal_question_options.id", ondelete="SET NULL"), nullable=True, index=True)
    answer_text: Mapped[str | None] = mapped_column(nullable=True)  # for TEXT/NUMBER/free-text answers
    option: Mapped[GoalQuestionOptions | None] = relationship("GoalQuestionOptions")
    question: Mapped[GoalQuestions] = relationship("GoalQuestions")