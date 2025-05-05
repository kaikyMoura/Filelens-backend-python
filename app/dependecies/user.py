from fastapi import Depends
from app.database import get_db
from sqlalchemy.ext.asyncio import AsyncSession

from app.services.user_service import UserService


def get_user_service(db: AsyncSession = Depends(get_db)):
    return UserService(db)
