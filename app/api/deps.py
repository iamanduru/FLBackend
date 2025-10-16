from fastapi import Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import Annotated
import jwt

from app.db.session import SessionLocal
from app.db.models import User
from app.core.config import settings

async def get_db() -> AsyncSession:
    async with SessionLocal() as session:
        yield session
        
DBSession = Annotated[AsyncSession, Depends(get_db)]

def get_current_user_factory(token_type: str = "access"):
    async def get_current_user(authorization: str | None, db: DBSession):
        if not authorization or not authorization.lower().startswith("bearer"):
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Missing token")
        token = authorization.split(" ", 1)[1]
        try:
            payload = jwt.decode(token, settings.jwt_secret, algorithms=[settings.jwt_alg])
            if payload.get("typ") != token_type:
                raise HTTPException(status_code=401, detail="Wrong token type")
            sub = payload.get("sub")
        except Exception:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
        
        result = await db.execute(select(User).where(User.id == int(sub)))
        user = result.scalar_one_or_none()
        if not user:
            raise HTTPException(status_code=401, detail="User not found")
        return user
    
    return get_current_user

get_current_user = get_current_user_factory("access")