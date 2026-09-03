from sqlalchemy import Column, Integer, String, Float, DateTime

from app.database.database import Base


class GroundTruth(Base):
    __tablename__ = "ground_truth"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    payment_id = Column(
        String,
        unique=True,
        index=True
    )

    expected_status = Column(
        String,
        index=True
    )

    expected_exception = Column(
        String,
        nullable=True
    )

    expected_amount = Column(
        Float,
        nullable=True
    )

    description = Column(
        String,
        nullable=True
    )

    created_at = Column(
        DateTime
    )