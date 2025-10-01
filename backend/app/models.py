"""Database models for JourneyLens."""

from __future__ import annotations

from datetime import UTC, datetime
from typing import Optional

from sqlalchemy import Boolean, Column, DateTime, Float, ForeignKey, Integer, String, Text, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .database import Base


class TimestampMixin:
    """Provides created/updated timestamp columns."""

    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(UTC))
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(UTC), onupdate=lambda: datetime.now(UTC)
    )


class Account(Base, TimestampMixin):
    __tablename__ = "accounts"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String, index=True)
    industry: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    status: Mapped[str] = mapped_column(String, default="active")

    contacts: Mapped[list["Contact"]] = relationship("Contact", back_populates="account", cascade="all, delete-orphan")
    interactions: Mapped[list["Interaction"]] = relationship("Interaction", back_populates="account", cascade="all, delete-orphan")


class Contact(Base, TimestampMixin):
    __tablename__ = "contacts"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    account_id: Mapped[int] = mapped_column(ForeignKey("accounts.id"), index=True)
    name: Mapped[str] = mapped_column(String)
    email: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    role: Mapped[Optional[str]] = mapped_column(String, nullable=True)

    account: Mapped[Account] = relationship("Account", back_populates="contacts")
    interactions: Mapped[list["Interaction"]] = relationship("Interaction", back_populates="contact")


class Interaction(Base, TimestampMixin):
    __tablename__ = "interactions"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    account_id: Mapped[int] = mapped_column(ForeignKey("accounts.id"), index=True)
    contact_id: Mapped[Optional[int]] = mapped_column(ForeignKey("contacts.id"), nullable=True, index=True)
    channel: Mapped[str] = mapped_column(String)
    content: Mapped[str] = mapped_column(Text)
    summary: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    timestamp: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(UTC))
    source_file: Mapped[Optional[str]] = mapped_column(String, nullable=True)

    account: Mapped[Account] = relationship("Account", back_populates="interactions")
    contact: Mapped[Optional[Contact]] = relationship("Contact", back_populates="interactions")
    insight: Mapped[Optional["Insight"]] = relationship("Insight", back_populates="interaction", uselist=False, cascade="all, delete-orphan")


class Insight(Base, TimestampMixin):
    __tablename__ = "insights"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    interaction_id: Mapped[int] = mapped_column(ForeignKey("interactions.id"), unique=True)
    intent: Mapped[str] = mapped_column(String, index=True)
    sentiment: Mapped[str] = mapped_column(String, index=True)
    risk_score: Mapped[float] = mapped_column(Float)
    confidence: Mapped[float] = mapped_column(Float, default=0.5)
    summary: Mapped[str] = mapped_column(Text)
    keywords: Mapped[Optional[str]] = mapped_column(String, nullable=True)

    interaction: Mapped[Interaction] = relationship("Interaction", back_populates="insight")
    feedback_items: Mapped[list["Feedback"]] = relationship("Feedback", back_populates="insight", cascade="all, delete-orphan")


class Feedback(Base, TimestampMixin):
    __tablename__ = "feedback"
    __table_args__ = (UniqueConstraint("insight_id", "user_id", name="uq_feedback_per_user"),)

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    insight_id: Mapped[int] = mapped_column(ForeignKey("insights.id"))
    user_id: Mapped[str] = mapped_column(String)
    rating: Mapped[bool] = mapped_column(Boolean)
    reason_code: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    comments: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    insight: Mapped[Insight] = relationship("Insight", back_populates="feedback_items")


class EvalSample(Base, TimestampMixin):
    __tablename__ = "eval_samples"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    interaction_id: Mapped[int] = mapped_column(ForeignKey("interactions.id"), unique=True)
    expected_intent: Mapped[str] = mapped_column(String)
    expected_sentiment: Mapped[str] = mapped_column(String)
    expected_risk: Mapped[float] = mapped_column(Float)

    interaction: Mapped[Interaction] = relationship("Interaction")
