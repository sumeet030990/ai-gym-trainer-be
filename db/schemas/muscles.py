from db.database import Base
import uuid
from sqlalchemy.orm import Mapped, mapped_column 

class Muscles(Base):
    __tablename__ = "muscles"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    name: Mapped[str] = mapped_column(nullable=False)
    description: Mapped[str | None] = mapped_column(nullable=True)