from typing import Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.db.models import Rule

async def pick_category_for_row(
    db: AsyncSession,
    user_id: int,
    merchant: Optional[str],
    memo: Optional[str],
    amount: float,
) -> Optional[int]:
    """
    Applies simple rule precedence:
    1) merchant contains pattern
    2) memo contains pattern
    3) amount_range "min-max"
    Returns category_id or None.
    """
    res = await db.execute(select(Rule).where(Rule.user_id == user_id, Rule.enabled == True))  # noqa: E712
    rules = res.scalars().all()

    m_lower = (merchant or "").lower()
    memo_lower = (memo or "").lower()

    # merchant contains
    for r in rules:
        if r.scope == "merchant" and r.pattern.lower() in m_lower:
            return r.category_id

    # memo contains
    for r in rules:
        if r.scope == "memo" and r.pattern.lower() in memo_lower:
            return r.category_id

    # amount range
    for r in rules:
        if r.scope == "amount_range":
            try:
                parts = r.pattern.split("-")
                lo = float(parts[0]) if parts[0] else None
                hi = float(parts[1]) if len(parts) > 1 and parts[1] else None
                if (lo is None or amount >= lo) and (hi is None or amount <= hi):
                    return r.category_id
            except Exception:
                continue

    return None
