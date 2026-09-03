from sqlalchemy import Column, Integer, Float, DateTime
from datetime import datetime

from app.database.database import Base


class EvaluationRun(Base):
    __tablename__ = "evaluation_runs"

    id = Column(Integer, primary_key=True, index=True)

    total_records = Column(Integer, default=0)

    correct_status = Column(Integer, default=0)
    incorrect_status = Column(Integer, default=0)

    true_positives = Column(Integer, default=0)
    false_positives = Column(Integer, default=0)
    false_negatives = Column(Integer, default=0)

    accuracy = Column(Float, default=0.0)
    precision = Column(Float, default=0.0)
    recall = Column(Float, default=0.0)
    f1_score = Column(Float, default=0.0)

    exception_detection_rate = Column(Float, default=0.0)
    false_match_rate = Column(Float, default=0.0)
    exception_type_accuracy = Column(Float, default=0.0)

    processing_time_seconds = Column(Float, default=0.0)
    records_per_second = Column(Float, default=0.0)

    evaluated_at = Column(
        DateTime,
        default=datetime.utcnow
    )