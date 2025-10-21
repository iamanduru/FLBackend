from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, insert, delete
from typing import List

from app.core.deps import get_db, get_current_user
from app.db.models import Account
from app.schemas.account import AccountCreate, AccountOut

router = APIRouter(prefix="/accounts", tags=["accounts"])

@router.get("", response_model=List[AccountOut])
async def list_accounts(db: AsyncSession = Depends(get_db), user=Depends(get_current_user)):
    res = await db.execute(select(Account).where(Account.user_id == user.id).order_by(Account.created_at.desc()))
    return res.scalars().all()

@router.post("", response_model=AccountOut, status_code=201)
async def create_account(payload: AccountCreate, db: AsyncSession = Depends(get_db), user=Depends(get_current_user)):
    stmt = insert(Account).values(
        user_id=user.id,
        provider=payload.provider,
        display_name=payload.display_name,
        meta=payload.meta,
    ).returning(Account)
    result = await db.execute(stmt)
    await db.commit()
    return result.scalar_one()

@router.delete("/{account_id}", status_code=204)
async def delete_account(account_id: int, db: AsyncSession = Depends(get_db), user=Depends(get_current_user)):
    # hard delete is fine for now (no foreign key cascade)
    # prevent deleting accounts that still have transactions
    from sqlalchemy import select, func
    from app.db.models import Transaction
    count_res = await db.execute(
        select (func.count()).select_from(Transaction).where(
            Transaction.user_id == user.id, Transaction.account_id == account_id
        )
    )
    if count_res.scalar_one() > 0:
        raise HTTPException(status_code=409, detail="Account has transactions")
    res = await db.execute(
        delete(Account).where(Account.id == account_id, Account.user_id == user.id)
    )
    await db.commit()
    if res.rowcount == 0:
        raise HTTPException(status_code=404, detail="Not Found")