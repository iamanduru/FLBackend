from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update, and_
from typing import List, Optional
from datetime import datetime

from app.core.deps import get_db, get_current_user
from app.db.models import Transaction

router = APIRouter(prefix="/transactions", tags=["transactions"])

@router.get("", response_model=List["TransactionOut"])
async def list_transactions(
    db: AsyncSession = Depends(get_db),
    user=Depends(get_current_user),
    account_id: Optional[int] = None,
    category_id: Optional[int] = None,
    date_from: Optional[datetime] = Query(None),
    date_to: Optional[datetime] = Query(None),
    limit: int = Query(100, ge=1, le=1000),
    offset: int = Query(0, ge=0),
):
    from app.schemas.transaction import TransactionOut  # avoid circular import in FastAPI openapi build

    conds = [Transaction.user_id == user.id]
    if account_id:
        conds.append(Transaction.account_id == account_id)
    if category_id:
        conds.append(Transaction.category_id == category_id)
    if date_from:
        conds.append(Transaction.txn_time >= date_from)
    if date_to:
        conds.append(Transaction.txn_time < date_to)

    stmt = (
        select(Transaction)
        .where(and_(*conds))
        .order_by(Transaction.txn_time.desc(), Transaction.id.desc())
        .limit(limit)
        .offset(offset)
    )
    res = await db.execute(stmt)
    return [TransactionOut.model_validate(t) for t in res.scalars().all()]

@router.patch("/{txn_id}", response_model="TransactionOut")
async def patch_transaction(
    txn_id: int,
    body: "TransactionPatch",
    db: AsyncSession = Depends(get_db),
    user=Depends(get_current_user),
):
    from app.schemas.transaction import TransactionPatch, TransactionOut
    updates = {}
    if body.category_id is not None:
        updates["category_id"] = body.category_id
    if body.memo is not None:
        updates["memo"] = body.memo
    if body.locked is not None:
        updates["locked"] = body.locked

    if not updates:
        raise HTTPException(status_code=400, detail="No fields to update")

    stmt = (
        update(Transaction)
        .where(Transaction.id == txn_id, Transaction.user_id == user.id)
        .values(**updates)
        .returning(Transaction)
    )
    res = await db.execute(stmt)
    row = res.scalar_one_or_none()
    if not row:
        raise HTTPException(status_code=404, detail="Not found")
    await db.commit()
    return TransactionOut.model_validate(row)
