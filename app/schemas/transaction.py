from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from decimal import Decimal

class TransactionOut(BaseModel):
    id: int
    account_id: int
    txn_time: datetime
    amount: Decimal
    currency: str
    type: str
    merchant: Optional[str] = None
    memo: Optional[str] = None
    category_id: Optional[int] = None
    balance_after: Optional[Decimal] = None
    model_confidence: Optional[float] = None
    locked: bool
    class Config: from_attributes = True

class TransactionPatch(BaseModel):
    category_id: Optional[int] = None
    memo: Optional[str] = None
    locked: Optional[bool] = None
