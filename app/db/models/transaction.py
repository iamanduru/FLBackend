# app/db/models/transaction.py
from datetime import datetime
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import (
    String, DateTime, func, BigInteger, JSON, DECIMAL, Boolean, ForeignKey, CHAR
)
from app.db.session import Base

class Transaction(Base):
    __tablename__ = "transactions"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(BigInteger, ForeignKey("users.id"), nullable=False, index=True)
    account_id: Mapped[int] = mapped_column(BigInteger, ForeignKey("accounts.id"), nullable=False, index=True)

    txn_time: Mapped[datetime] = mapped_column(DateTime, nullable=False)            # UTC
    amount: Mapped[float] = mapped_column(DECIMAL(14, 2), nullable=False)
    currency: Mapped[str] = mapped_column(String(3), nullable=False)                # ISO-4217
    type: Mapped[str] = mapped_column(String(10), nullable=False)                   # debit|credit

    merchant: Mapped[str | None] = mapped_column(String(160))
    memo: Mapped[str | None] = mapped_column(String(255))
    category_id: Mapped[int | None] = mapped_column(BigInteger, ForeignKey("categories.id"))
    balance_after: Mapped[float | None] = mapped_column(DECIMAL(14, 2))

    source: Mapped[str] = mapped_column(String(20), nullable=False)                 # csv|sms|api
    raw: Mapped[dict | None] = mapped_column(JSON)
    model_confidence: Mapped[float | None] = mapped_column(DECIMAL(5, 4))
    locked: Mapped[bool] = mapped_column(Boolean, default=False, server_default="0")

    txn_hash: Mapped[str | None] = mapped_column(CHAR(64), index=True)              # for dedupe

    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now(), onupdate=func.now())
