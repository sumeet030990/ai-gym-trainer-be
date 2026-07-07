from datetime import datetime
import uuid
from sqlalchemy import ForeignKey, UniqueConstraint, func
from sqlalchemy.orm import Mapped, mapped_column

from db.database import Base


class UserAnswers(Base):
    __tablename__ = "user_answers"
    __table_args__ = (UniqueConstraint("user_id", "question_id", "option_id", name="uq_user_question_option"),)

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    user_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("users.id"), nullable=False)
    question_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("questions.id"), nullable=False)
    option_id: Mapped[uuid.UUID | None] = mapped_column(ForeignKey("question_options.id"), nullable=True)
    answer_text: Mapped[str | None] = mapped_column(nullable=True)  # for TEXT/NUMBER/free-text answers
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(server_default=func.now(), onupdate=func.now())
