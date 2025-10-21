from pyndantic import BaseModel, Field
from typing import Optional, Any

class AccountCreate(BaseModel):
    provider: str = Field(examples=["mpesa", "ncba", "csv"])
    display_name: str
    meta: Optional[dict[str, Any]] = None
    
class AccountOut(BaseModel):
    id: int
    provider: str
    display_name: str
    meta: Optional[dict] = None
    class Config: from_attributes = True