import datetime as dt
from typing import TYPE_CHECKING

from sqlalchemy import BIGINT, SMALLINT, CheckConstraint, String, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base, TimestampMixin

if TYPE_CHECKING:
    from .diary import DiaryRecord


class User(Base, TimestampMixin):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(BIGINT, primary_key=True, autoincrement=False)
    username: Mapped[str | None] = mapped_column(String(128))
    full_name: Mapped[str] = mapped_column(String(128))
    call_name: Mapped[str | None] = mapped_column(String(128))
    age: Mapped[int | None] = mapped_column(
        SMALLINT, CheckConstraint("age >= 0", name="age_positive")
    )
    last_diary_sent: Mapped[dt.datetime | None] = mapped_column(DateTime, default=None)

    diary_records: Mapped[list["DiaryRecord"]] = relationship(back_populates="user")

    def __repr__(self):
        return f"<User {self.id} {self.username} {self.full_name}>"
