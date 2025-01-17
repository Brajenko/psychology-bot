from sqlalchemy import Column, String, ForeignKey, Table, Text, SMALLINT
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base, IdMixin, TimestampMixin


class Poll(IdMixin, Base):
    __tablename__ = "polls"

    name: Mapped[str] = mapped_column(String(255))
    intro: Mapped[str | None] = mapped_column(Text())
    is_psychological: Mapped[bool]
    questions: Mapped[list["Question"]] = relationship(back_populates="poll")
    completions: Mapped[list["Completion"]] = relationship(back_populates="poll")


question2variant = Table(
    "question_to_variant",
    Base.metadata,
    Column("question_id", ForeignKey("questions.id")),
    Column("variant_id", ForeignKey("variants.id")),
)


class Question(IdMixin, Base):
    __tablename__ = "questions"

    poll_id: Mapped[int] = mapped_column(ForeignKey("polls.id"))
    poll: Mapped["Poll"] = relationship(back_populates="questions")

    variants: Mapped[list["Variant"]] = relationship(secondary=question2variant)

    content: Mapped[str] = mapped_column(String(255))


class Variant(IdMixin, Base):
    __tablename__ = "variants"

    content: Mapped[str] = mapped_column(String(255))
    points: Mapped[int] = mapped_column(SMALLINT)


class Completion(IdMixin, TimestampMixin, Base):
    __tablename__ = "completions"

    poll_id: Mapped[int] = mapped_column(ForeignKey("polls.id"))
    poll: Mapped["Poll"] = relationship(back_populates="completions")

    score: Mapped[int]


class Result(IdMixin, Base):
    __tablename__ = "results"

    poll_id: Mapped[int] = mapped_column(ForeignKey("polls.id"))
    poll: Mapped["Poll"] = relationship()

    content: Mapped[str] = mapped_column(String(255))

    min_points: Mapped[int] = mapped_column(SMALLINT)
    max_points: Mapped[int] = mapped_column(SMALLINT)
