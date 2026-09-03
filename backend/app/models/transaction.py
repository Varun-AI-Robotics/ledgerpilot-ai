from sqlalchemy import Column, Integer, String, Float, DateTime
from app.database.database import Base


class Payment(Base):
    __tablename__ = "payments"

    id = Column(Integer, primary_key=True, index=True)

    payment_id = Column(String, unique=True, index=True)
    order_id = Column(String)

    amount = Column(Float)
    currency = Column(String)

    payment_method = Column(String)
    payment_status = Column(String)

    created_at = Column(DateTime)


class Settlement(Base):
    __tablename__ = "settlements"

    id = Column(Integer, primary_key=True, index=True)

    settlement_id = Column(String, unique=True, index=True)

    payment_id = Column(String, index=True)

    gross_amount = Column(Float)
    fee = Column(Float)
    tax = Column(Float)
    net_amount = Column(Float)

    settlement_status = Column(String)

    settlement_date = Column(DateTime)


class BankTransaction(Base):
    __tablename__ = "bank_transactions"

    id = Column(Integer, primary_key=True, index=True)

    bank_transaction_id = Column(String, unique=True, index=True)

    payment_id = Column(String, index=True)

    reference = Column(String)

    amount = Column(Float)

    transaction_type = Column(String)

    transaction_date = Column(DateTime)