from sqlalchemy import BIGINT, SMALLINT, CheckConstraint, String
from sqlalchemy.orm import Mapped, mapped_column

from .base import Base, TimestampMixin


class User(Base, TimestampMixin):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(BIGINT, primary_key=True, autoincrement=False)
    username: Mapped[str | None] = mapped_column(String(128))
    full_name: Mapped[str] = mapped_column(String(128))
    call_name: Mapped[str | None] = mapped_column(String(128))
    age: Mapped[int | None] = mapped_column(
        SMALLINT, CheckConstraint("age >= 0", name="age_positive")
    )

    def __repr__(self):
        return f"<User {self.id} {self.username} {self.full_name}>"
