"""Pydantic schemas for JourneyLens API."""

from __future__ import annotations

from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, Field, ConfigDict


class Contact(BaseModel):
    id: int
    account_id: int
    name: str
    email: Optional[str]
    role: Optional[str]
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)  # type: ignore[call-arg]


class Insight(BaseModel):
    id: int
    interaction_id: int
    intent: str
    sentiment: str
    risk_score: float
    confidence: float
    summary: str
    keywords: Optional[str]
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)  # type: ignore[call-arg]


class Interaction(BaseModel):
    id: int
    account_id: int
    contact_id: Optional[int]
    channel: str
    content: str
    summary: Optional[str]
    timestamp: datetime
    created_at: datetime
    updated_at: datetime
    source_file: Optional[str]
    insight: Optional[Insight]

    model_config = ConfigDict(from_attributes=True)  # type: ignore[call-arg]


class InteractionCreate(BaseModel):
    account_id: int
    contact_id: Optional[int] = Field(default=None)
    channel: str = Field(default="email", description="Interaction channel, e.g. email, call, chat")
    content: str = Field(..., min_length=1)
    timestamp: Optional[datetime] = None


class FeedbackCreate(BaseModel):
    insight_id: int
    rating: bool
    reason_code: str
    comments: Optional[str] = None


class Feedback(BaseModel):
    id: int
    insight_id: int
    user_id: str
    rating: bool
    reason_code: Optional[str]
    comments: Optional[str]
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)  # type: ignore[call-arg]


class Account(BaseModel):
    id: int
    name: str
    industry: Optional[str]
    status: str
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)  # type: ignore[call-arg]


class AccountWithInsights(Account):
    interactions: List[Interaction]


class DashboardAccount(BaseModel):
    account_id: int
    account_name: str
    risk_score: float
    recent_interactions: int
    last_interaction: Optional[datetime]
    next_action: str


class EvaluationMetrics(BaseModel):
    ai_coverage: float
    feedback_rate: float
    useful_rate: float
    total_insights: int
    avg_confidence: float
    performance_trend: str


class RagResponse(BaseModel):
    account_id: int
    query: str
    answer: str
    supporting_insights: List[Insight] = Field(default_factory=list)
    timestamp: datetime