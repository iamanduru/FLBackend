from datetime import datetime
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import DateTime, func, BigInteger, JSON, CHAR, UniqueConstraint, Text  # ← use Text
from app.db.session import Base

class Summary(Base):
    __tablename__ = "summaries"
    __table_args__ = (
        UniqueConstraint("user_id", "month", name="uq_summaries_user_month"),
        # If you had Index("ix_summaries_user", "user_id"), remove it to avoid dup index
    )

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(BigInteger, nullable=False, index=True)  # keep index=True
    month: Mapped[str] = mapped_column(CHAR(7), nullable=False)
    kpis: Mapped[dict] = mapped_column(JSON, nullable=False)
    summary_text: Mapped[str] = mapped_column(Text, nullable=False)               # ← TEXT, not String(65535)
    forecast: Mapped[dict | None] = mapped_column(JSON)
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())
