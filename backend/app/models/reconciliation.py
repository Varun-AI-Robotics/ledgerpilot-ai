from sqlalchemy import Column, Integer, String, Float, DateTime
from app.database.database import Base


class Reconciliation(Base):

    __tablename__ = "reconciliations"

    id = Column(Integer, primary_key=True, index=True)

    payment_id = Column(String, index=True)

    payment_amount = Column(Float)

    settlement_amount = Column(Float, nullable=True)

    bank_amount = Column(Float, nullable=True)

    expected_net_amount = Column(Float, nullable=True)

    fee = Column(Float, nullable=True)

    tax = Column(Float, nullable=True)

    amount_difference = Column(Float, nullable=True)

    reference_match = Column(Integer, default=0)

    settlement_found = Column(Integer, default=0)

    bank_transaction_found = Column(Integer, default=0)

    status = Column(String, index=True)

    reason = Column(String)

    reconciled_at = Column(DateTime)