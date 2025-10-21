from fastapi import APIRouter, Depends
from app.core.deps import get_current_user
from app.db.models import User

router = APIRouter(prefix="/users", tags=["users"])

@router.get("/me")
async def me(user: User = Depends(get_current_user)):
    return {"id": user.id, "email": user.email, "name": user.name }