from typing import List, TYPE_CHECKING

from sqlalchemy.orm import Mapped, mapped_column, relationship

from db.database import Base
from db.mixins import TimestampMixin, UUIDPrimaryKeyMixin

if TYPE_CHECKING:
    from db.schemas.goal_questions import GoalQuestions


class Categories(UUIDPrimaryKeyMixin, TimestampMixin, Base):
    __tablename__ = "categories"

    name: Mapped[str] = mapped_column(nullable=False)
    sort_order: Mapped[int | None] = mapped_column(nullable=True)
    questions: Mapped[List["GoalQuestions"]] = relationship(
        "GoalQuestions", back_populates="category", order_by="GoalQuestions.sort_order"
    )
