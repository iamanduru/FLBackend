from datetime import datetime                    # ← add this
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, DateTime, func, BigInteger, Boolean, ForeignKey
from app.db.session import Base

class Rule(Base):
    __tablename__ = "rules"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(BigInteger, ForeignKey("users.id"), nullable=False, index=True)
    category_id: Mapped[int] = mapped_column(BigInteger, ForeignKey("categories.id"), nullable=False)
    scope: Mapped[str] = mapped_column(String(30), nullable=False)      # merchant|memo|amount_range
    pattern: Mapped[str] = mapped_column(String(255), nullable=False)
    enabled: Mapped[bool] = mapped_column(Boolean, default=True, server_default="1")
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())
