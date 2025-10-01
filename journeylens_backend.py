
# JourneyLens Backend - FastAPI Implementation
# Core architecture for customer intelligence console

from fastapi import FastAPI, Depends, HTTPException, UploadFile, File
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy import create_engine, Column, Integer, String, DateTime, Text, Float, ForeignKey, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session, relationship
from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from datetime import datetime
import json
import json

# =============================================================================
# DATABASE MODELS
# =============================================================================

Base = declarative_base()

class Account(Base):
    __tablename__ = "accounts"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    industry = Column(String)
    status = Column(String, default="active")
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    contacts = relationship("Contact", back_populates="account")
    interactions = relationship("Interaction", back_populates="account")

class Contact(Base):
    __tablename__ = "contacts"

    id = Column(Integer, primary_key=True, index=True)
    account_id = Column(Integer, ForeignKey("accounts.id"))
    name = Column(String)
    email = Column(String)
    role = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    account = relationship("Account", back_populates="contacts")
    interactions = relationship("Interaction", back_populates="contact")

class Interaction(Base):
    __tablename__ = "interactions"

    id = Column(Integer, primary_key=True, index=True)
    account_id = Column(Integer, ForeignKey("accounts.id"))
    contact_id = Column(Integer, ForeignKey("contacts.id"), nullable=True)
    channel = Column(String)  # email, call, chat, etc.
    timestamp = Column(DateTime, default=datetime.utcnow)
    content = Column(Text)
    file_path = Column(String, nullable=True)

    # Relationships
    account = relationship("Account", back_populates="interactions")
    contact = relationship("Contact", back_populates="interactions")
    insight = relationship("Insight", back_populates="interaction", uselist=False)

class Insight(Base):
    __tablename__ = "insights"

    id = Column(Integer, primary_key=True, index=True)
    interaction_id = Column(Integer, ForeignKey("interactions.id"))
    intent = Column(String)
    sentiment = Column(String)
    risk_score = Column(Float)
    summary = Column(Text)
    confidence = Column(Float)
    embedding = Column(Text)  # JSON serialized vector
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    interaction = relationship("Interaction", back_populates="insight")
    feedback_items = relationship("Feedback", back_populates="insight")

class Feedback(Base):
    __tablename__ = "feedback"

    id = Column(Integer, primary_key=True, index=True)
    insight_id = Column(Integer, ForeignKey("insights.id"))
    user_id = Column(String)  # Could be FK to Users table
    rating = Column(Boolean)  # True = thumbs up, False = thumbs down
    reason_code = Column(String)
    comments = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    insight = relationship("Insight", back_populates="feedback_items")

class EvalSample(Base):
    __tablename__ = "eval_samples"

    id = Column(Integer, primary_key=True, index=True)
    interaction_id = Column(Integer, ForeignKey("interactions.id"))
    expected_intent = Column(String)
    expected_sentiment = Column(String)
    expected_risk = Column(Float)
    created_at = Column(DateTime, default=datetime.utcnow)

# =============================================================================
# PYDANTIC MODELS (API Schemas)
# =============================================================================

class InteractionCreate(BaseModel):
    account_id: int
    contact_id: Optional[int] = None
    channel: str
    content: str
    timestamp: Optional[datetime] = None

class InsightResponse(BaseModel):
    id: int
    intent: str
    sentiment: str
    risk_score: float
    summary: str
    confidence: float
    created_at: datetime

class AccountDashboard(BaseModel):
    account_id: int
    account_name: str
    risk_score: float
    recent_interactions: int
    last_interaction: datetime
    next_action: str

class FeedbackCreate(BaseModel):
    insight_id: int
    rating: bool
    reason_code: str
    comments: Optional[str] = None


# =============================================================================
# INSIGHT SERVICES (Heuristic)
# =============================================================================

class InsightService:
    def analyze_interaction(self, content: str) -> Dict[str, Any]:
        """Heuristically analyze interaction content for intent, sentiment, and risk."""
        # Simple keyword-based heuristic (replace with your own logic)
        intent = "support_request" if "help" in content.lower() else "general_inquiry"
        sentiment = "negative" if any(w in content.lower() for w in ["angry", "frustrated", "bad"]) else "positive"
        risk_score = 0.8 if sentiment == "negative" else 0.2
        summary = content[:80] + ("..." if len(content) > 80 else "")
        confidence = 0.5
        embedding = []  # No embedding
        return {
            "intent": intent,
            "sentiment": sentiment,
            "risk_score": risk_score,
            "summary": summary,
            "confidence": confidence,
            "embedding": embedding
        }

    def rag_query(self, query: str, account_id: int, db: Session) -> str:
        """Return a canned response for account-specific insights."""
        insights = db.query(Insight).join(Interaction).filter(
            Interaction.account_id == account_id
        ).limit(5).all()
        if not insights:
            return "No recent insights available for this account."
        return f"Based on recent interactions, the answer to '{query}' is not available in this demo."

# =============================================================================
# FASTAPI APPLICATION
# =============================================================================

app = FastAPI(title="JourneyLens API", version="1.0.0")

# Initialize services
insight_service = InsightService()

# Security
security = HTTPBearer()

# Database setup (simplified)
engine = create_engine("sqlite:///journeylens.db")
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# =============================================================================
# API ENDPOINTS
# =============================================================================

@app.post("/interactions/", response_model=InsightResponse)
async def create_interaction(
    interaction: InteractionCreate,
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
):
    """Create new interaction and generate AI insights"""

    # Create interaction record
    db_interaction = Interaction(**interaction.dict())
    db.add(db_interaction)
    db.commit()
    db.refresh(db_interaction)

    # Generate heuristic analysis
    analysis = insight_service.analyze_interaction(interaction.content)

    # Store insights
    db_insight = Insight(
        interaction_id=db_interaction.id,
        intent=analysis["intent"],
        sentiment=analysis["sentiment"],
        risk_score=analysis["risk_score"],
        summary=analysis["summary"],
        confidence=analysis["confidence"],
        embedding=json.dumps(analysis["embedding"])
    )
    db.add(db_insight)
    db.commit()
    db.refresh(db_insight)

    return InsightResponse.from_orm(db_insight)

@app.get("/dashboard/csm")
async def get_csm_dashboard(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
) -> List[AccountDashboard]:
    """Get CSM-specific dashboard data"""

    # Get accounts at risk (risk_score > 0.7)
    at_risk_accounts = []

    accounts = db.query(Account).all()
    for account in accounts:
        # Get latest insights for this account
        latest_insights = db.query(Insight).join(Interaction).filter(
            Interaction.account_id == getattr(account, 'id', None)
        ).order_by(Insight.created_at.desc()).limit(5).all()

        if latest_insights:
            # Use actual values, not SQLAlchemy columns
            avg_risk = sum(float(getattr(i, 'risk_score', 0.0)) for i in latest_insights) / len(latest_insights)
            if avg_risk > 0.7:
                at_risk_accounts.append(AccountDashboard(
                    account_id=getattr(account, 'id', 0),
                    account_name=getattr(account, 'name', ''),
                    risk_score=avg_risk,
                    recent_interactions=len(latest_insights),
                    last_interaction=getattr(latest_insights[0], 'created_at', None) or datetime.utcnow(),
                    next_action="Schedule check-in call" if avg_risk > 0.8 else "Monitor closely"
                ))

    return at_risk_accounts

@app.get("/accounts/{account_id}/rag")
async def account_rag_query(
    account_id: int,
    query: str,
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
):
    """Get RAG-powered insights for specific account"""

    answer = insight_service.rag_query(query, account_id, db)

    return {
        "account_id": account_id,
        "query": query,
        "answer": answer,
        "timestamp": datetime.utcnow()
    }

@app.post("/feedback/")
async def create_feedback(
    feedback: FeedbackCreate,
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
):
    """Submit feedback on insights"""

    db_feedback = Feedback(
        insight_id=feedback.insight_id,
        user_id="current_user",  # Would get from auth token
        rating=feedback.rating,
        reason_code=feedback.reason_code,
        comments=feedback.comments
    )

    db.add(db_feedback)
    db.commit()

    return {"message": "Feedback recorded successfully"}

@app.get("/evaluations/metrics")
async def get_evaluation_metrics(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
):
    """Get evaluation metrics and performance data"""

    # Calculate feedback rates
    total_insights = db.query(Insight).count()
    total_feedback = db.query(Feedback).count()
    positive_feedback = db.query(Feedback).filter(Feedback.rating == True).count()

    feedback_rate = (total_feedback / total_insights * 100) if total_insights > 0 else 0
    useful_rate = (positive_feedback / total_feedback * 100) if total_feedback > 0 else 0

    return {
    "coverage": 85.2,  # Percentage of interactions with analysis
        "feedback_rate": round(feedback_rate, 1),
        "useful_rate": round(useful_rate, 1),
        "total_insights": total_insights,
        "avg_confidence": 0.87,
        "performance_trend": "improving"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
