import typing
from datetime import datetime

from sqlalchemy import (
    BOOLEAN,
    CHAR,
    TIMESTAMP,
    Float,
    ForeignKey,
    Integer,
    String,
    UniqueConstraint,
)
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship

# from src.database import Base


class Base(DeclarativeBase):
    pass


class IDDateTimeMixin(object):
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    created_at = mapped_column(TIMESTAMP(timezone=True), default=datetime.now)


class Drug(IDDateTimeMixin, Base):
    __tablename__ = "drug"

    name: Mapped[str] = mapped_column(String)
    dosage: Mapped[float] = mapped_column(Float)
    units: Mapped[str] = mapped_column(String)
    pills: Mapped[typing.List["Pill"]] = relationship("Pill", back_populates="drug")


class BeforeAfterDuringMeals(IDDateTimeMixin, Base):
    __tablename__ = "meal"

    relation: Mapped[str] = mapped_column(String)  # До/После/Во_время еды
    timedelta: Mapped[int] = mapped_column(Integer, nullable=True)
    pill: Mapped["Pill"] = relationship("Pill", back_populates="meals")


class User(IDDateTimeMixin, Base):
    __tablename__ = "user"
    username: Mapped[str] = mapped_column(String)
    pills: Mapped[typing.List["Pill"]] = relationship("Pill", back_populates="user")


class Pill(IDDateTimeMixin, Base):
    __tablename__ = "pill"

    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"))
    user: Mapped["User"] = relationship("User", back_populates="pills")

    drug_id: Mapped[int] = mapped_column(ForeignKey("drug.id"))
    drug: Mapped["Drug"] = relationship("Drug", back_populates="pills")

    amount: Mapped[int] = mapped_column(Integer)
    half: Mapped[bool] = mapped_column(BOOLEAN, default=False)

    meal_id: Mapped[int] = mapped_column(ForeignKey("meal.id"))
    meals: Mapped[typing.List["BeforeAfterDuringMeals"]] = relationship(
        BeforeAfterDuringMeals, back_populates="pill"
    )
