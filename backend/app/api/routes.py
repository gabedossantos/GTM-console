"""FastAPI routes for the JourneyLens backend."""

from __future__ import annotations

from datetime import UTC, datetime
from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session, joinedload

from .. import schemas
from ..core.config import get_settings
from ..models import Account, Feedback, Insight, Interaction
from ..services.analysis import InsightEngine, NEXT_ACTIONS
from .deps import get_db_session, require_token

router = APIRouter()
settings = get_settings()
analysis_engine = InsightEngine()


@router.get("/health")
def health_check() -> dict[str, str | datetime]:
    """Simple health check endpoint without authentication."""

    return {"status": "ok", "timestamp": datetime.now(UTC), "version": settings.api_version}


@router.get("/accounts", response_model=List[schemas.Account])
def list_accounts(
    db: Session = Depends(get_db_session),
    _: str = Depends(require_token),
) -> List[Account]:
    """Return all accounts sorted by name."""

    return db.query(Account).order_by(Account.name.asc()).all()


@router.get("/accounts/{account_id}", response_model=schemas.AccountWithInsights)
def get_account_details(
    account_id: int,
    db: Session = Depends(get_db_session),
    _: str = Depends(require_token),
):
    """Retrieve account detail including interactions and insights."""

    account = (
        db.query(Account)
        .options(joinedload(Account.interactions).joinedload(Interaction.insight))
        .filter(Account.id == account_id)
        .first()
    )

    if not account:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Account not found")

    # Sort interactions by timestamp descending for timeline display
    account.interactions.sort(key=lambda interaction: interaction.timestamp, reverse=True)
    return account


@router.get("/dashboard/csm", response_model=List[schemas.DashboardAccount])
def get_csm_dashboard(
    db: Session = Depends(get_db_session),
    _: str = Depends(require_token),
) -> List[schemas.DashboardAccount]:
    """Aggregate risk insights for customer success managers."""

    dashboard_rows: list[schemas.DashboardAccount] = []

    accounts = db.query(Account).options(joinedload(Account.interactions).joinedload(Interaction.insight)).all()
    for account in accounts:
        insights = [interaction.insight for interaction in account.interactions if interaction.insight]
        if not insights:
            continue

        risk_scores = [insight.risk_score for insight in insights]
        avg_risk = sum(risk_scores) / len(risk_scores)
        last_interaction = max((interaction.timestamp for interaction in account.interactions), default=None)
        dominant_intent = max(
            (insight.intent for insight in insights),
            key=lambda intent: len([i for i in insights if i.intent == intent]),
        )
        dashboard_rows.append(
            schemas.DashboardAccount(
                account_id=account.id,
                account_name=account.name,
                risk_score=round(avg_risk, 2),
                recent_interactions=len(account.interactions),
                last_interaction=last_interaction,
                next_action=NEXT_ACTIONS.get(dominant_intent, "Follow up with the customer"),
            )
        )

    dashboard_rows.sort(key=lambda row: row.risk_score, reverse=True)
    return dashboard_rows


@router.post("/interactions", response_model=schemas.Insight, status_code=status.HTTP_201_CREATED)
def create_interaction(
    payload: schemas.InteractionCreate,
    db: Session = Depends(get_db_session),
    _: str = Depends(require_token),
) -> Insight:
    """Create a new interaction, run analysis, and persist insight."""

    account = db.query(Account).filter(Account.id == payload.account_id).first()
    if not account:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid account_id")

    interaction = Interaction(
        account_id=payload.account_id,
        contact_id=payload.contact_id,
        channel=payload.channel,
        content=payload.content,
    timestamp=payload.timestamp or datetime.now(UTC),
    )
    db.add(interaction)
    db.flush()

    analysis = analysis_engine.analyze(interaction.id, interaction.content)
    insight = Insight(
        interaction_id=interaction.id,
        intent=analysis["intent"],
        sentiment=analysis["sentiment"],
        risk_score=float(analysis["risk_score"]),
        confidence=float(analysis.get("confidence", 0.65)),
        summary=analysis["summary"],
        keywords=analysis.get("keywords"),
    )
    interaction.summary = insight.summary
    db.add(insight)
    db.commit()
    db.refresh(insight)

    return insight


@router.get("/accounts/{account_id}/rag", response_model=schemas.RagResponse)
def rag_query(
    account_id: int,
    query: str,
    db: Session = Depends(get_db_session),
    _: str = Depends(require_token),
) -> schemas.RagResponse:
    """Return a retrieval augmented answer using account insights."""

    account = (
        db.query(Account)
        .options(joinedload(Account.interactions).joinedload(Interaction.insight))
        .filter(Account.id == account_id)
        .first()
    )

    if not account:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Account not found")

    insights = [interaction.insight for interaction in account.interactions if interaction.insight]
    answer, supporting_insights = analysis_engine.rag_answer(query, insights)

    return schemas.RagResponse(
        account_id=account_id,
        query=query,
        answer=answer,
        supporting_insights=[schemas.Insight.model_validate(insight) for insight in supporting_insights],
        timestamp=datetime.now(UTC),
    )


@router.post("/feedback", response_model=schemas.Feedback, status_code=status.HTTP_201_CREATED)
def submit_feedback(
    payload: schemas.FeedbackCreate,
    db: Session = Depends(get_db_session),
    _: str = Depends(require_token),
) -> Feedback:
    """Record feedback on an insight."""

    insight = db.query(Insight).filter(Insight.id == payload.insight_id).first()
    if not insight:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid insight_id")

    feedback = Feedback(
        insight_id=payload.insight_id,
        user_id="demo-user",
        rating=payload.rating,
        reason_code=payload.reason_code,
        comments=payload.comments,
    )
    db.add(feedback)
    db.commit()
    db.refresh(feedback)

    return feedback


@router.get("/evaluations/metrics", response_model=schemas.EvaluationMetrics)
def evaluation_metrics(
    db: Session = Depends(get_db_session),
    _: str = Depends(require_token),
) -> schemas.EvaluationMetrics:
    """Provide basic analytics about AI coverage and feedback."""

    total_insights = db.query(Insight).count()
    total_feedback = db.query(Feedback).count()
    positive_feedback = db.query(Feedback).filter(Feedback.rating.is_(True)).count()

    feedback_rate = (total_feedback / total_insights) * 100 if total_insights else 0.0
    useful_rate = (positive_feedback / total_feedback) * 100 if total_feedback else 0.0

    return schemas.EvaluationMetrics(
        ai_coverage=85.0,
        feedback_rate=round(feedback_rate, 1),
        useful_rate=round(useful_rate, 1),
        total_insights=total_insights,
        avg_confidence=0.78,
        performance_trend="improving",
    )


@router.get("/insights/recent", response_model=List[schemas.Insight])
def recent_insights(
    limit: int = 10,
    db: Session = Depends(get_db_session),
    _: str = Depends(require_token),
) -> List[Insight]:
    """Return the most recent insights for quick access panels."""

    limit = max(1, min(limit, 50))
    return (
        db.query(Insight)
        .options(joinedload(Insight.interaction))
        .order_by(Insight.created_at.desc())
        .limit(limit)
        .all()
    )
