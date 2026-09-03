from sqlalchemy import (
    Column,
    Integer,
    String,
    Float,
    Text,
    DateTime
)

from app.database.database import Base


class AIAnalysis(Base):

    __tablename__ = "ai_analyses"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    payment_id = Column(
        String,
        index=True
    )

    classification = Column(
        String
    )

    confidence = Column(
        Float
    )

    reason = Column(
        Text
    )

    recommended_action = Column(
        Text
    )

    priority = Column(
        String
    )

    created_at = Column(
        DateTime
    )