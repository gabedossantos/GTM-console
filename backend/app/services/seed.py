"""Utilities to seed the database with demo CSV data."""

from __future__ import annotations

import csv
from datetime import datetime
from pathlib import Path
from typing import Dict

from sqlalchemy.orm import Session

from ..core.config import Settings
from ..models import Account, Contact, EvalSample, Insight, Interaction
from .analysis import ExpectedInsight, InsightEngine


def load_demo_data(session: Session, settings: Settings) -> None:
    """Populate the database with demo data if it's empty."""

    if session.query(Account).count() > 0:
        return

    expected_lookup = _load_expected_map(settings.demo_data_expected)
    engine = InsightEngine(expected_lookup)

    accounts = _load_accounts(settings.demo_data_accounts)
    session.bulk_save_objects(accounts)
    session.flush()

    contacts = _load_contacts(settings.demo_data_contacts)
    session.bulk_save_objects(contacts)
    session.flush()

    interactions = _load_interactions(settings.demo_data_interactions)
    session.bulk_save_objects(interactions)
    session.flush()

    for interaction in interactions:
        analysis = engine.analyze(interaction.id, interaction.content)
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
        session.add(insight)

    eval_samples = [
        EvalSample(
            interaction_id=interaction_id,
            expected_intent=insight.expected_intent,
            expected_sentiment=insight.expected_sentiment,
            expected_risk=float(insight.expected_risk),
        )
        for interaction_id, insight in expected_lookup.items()
    ]
    session.bulk_save_objects(eval_samples)

    session.commit()


def _load_accounts(path: Path) -> list[Account]:
    with path.open("r", encoding="utf-8") as fh:
        reader = csv.DictReader(fh)
        return [
            Account(
                id=int(row["id"]),
                name=row["name"],
                industry=row.get("industry"),
                status=row.get("status", "active"),
                created_at=_parse_datetime(row.get("created_at")),
            )
            for row in reader
        ]


def _load_contacts(path: Path) -> list[Contact]:
    with path.open("r", encoding="utf-8") as fh:
        reader = csv.DictReader(fh)
        return [
            Contact(
                id=int(row["id"]),
                account_id=int(row["account_id"]),
                name=row["name"],
                email=row.get("email"),
                role=row.get("role"),
                created_at=_parse_datetime(row.get("created_at")),
            )
            for row in reader
        ]


def _load_interactions(path: Path) -> list[Interaction]:
    interactions: list[Interaction] = []
    with path.open("r", encoding="utf-8") as fh:
        reader = csv.DictReader(fh)
        for row in reader:
            interactions.append(
                Interaction(
                    id=int(row["id"]),
                    account_id=int(row["account_id"]),
                    contact_id=int(row["contact_id"]) if row.get("contact_id") else None,
                    channel=row.get("channel", "email"),
                    content=row.get("content", ""),
                    timestamp=_parse_datetime(row.get("timestamp")),
                    source_file=None,
                )
            )
    return interactions


def _load_expected_map(path: Path) -> Dict[int, ExpectedInsight]:
    lookup: Dict[int, ExpectedInsight] = {}
    if not path.exists():
        return lookup

    with path.open("r", encoding="utf-8") as fh:
        reader = csv.DictReader(fh)
        for row in reader:
            interaction_id = int(row["interaction_id"])
            lookup[interaction_id] = ExpectedInsight(
                expected_intent=row.get("expected_intent", "support_request"),
                expected_sentiment=row.get("expected_sentiment", "neutral"),
                expected_risk=float(row.get("expected_risk_score", 0.5)),
            )
    return lookup


def _parse_datetime(value: str | None) -> datetime:
    if not value:
        return datetime.utcnow()
    try:
        return datetime.fromisoformat(value)
    except ValueError:
        return datetime.utcnow()
