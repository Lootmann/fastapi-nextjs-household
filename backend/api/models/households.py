import datetime

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from api.db import Base


class Household(Base):
    __tablename__ = "households"

    id: Mapped[int] = mapped_column(primary_key=True)
    amount: Mapped[int]
    registered_at: Mapped[datetime.datetime]

    # Category
    category_id: Mapped[int] = mapped_column(ForeignKey("categories.id"))

    # User
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))

    def __repr__(self) -> str:
        return f"<Household ({self.id}, {self.amount}, {self.registered_at})>"
