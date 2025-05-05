from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
import hashlib
from fastapi import HTTPException
import re
import uuid
from app.database import get_db
from app.models.user import User
from app.repositories.user_repository import UserRepository
from app.schemas import UserCreate

from app.utils.token import create_access_token


class UserService:

    def __init__(self, db: AsyncSession = Depends(get_db)):
        self.user_repository = UserRepository(db)

    async def get_user_by_email(self, email: str):
        if not email:
            raise HTTPException(status_code=400, detail="Missing required properties")

        if not re.match(r"^[^\s@]+@[^\s@]+\.[^\s@]+$", email):
            raise HTTPException(status_code=400, detail="Email format is invalid")

        user = await self.user_repository.find_by_email(email)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        return user

    async def get_user_by_id(self, id: str):
        if not id:
            raise HTTPException(status_code=400, detail="Missing required properties")

        user = await self.user_repository.find_by_id(id)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        return user

    async def do_user_login(self, email: str, password: str) -> str:
        if not email:
            raise HTTPException(status_code=400, detail="Missing required properties")

        if not re.match(r"^[^\s@]+@[^\s@]+\.[^\s@]+$", email):
            raise HTTPException(status_code=400, detail="Missing required properties")

        if not password:
            raise HTTPException(status_code=400, detail="Missing required properties")

        user = await self.user_repository.find_by_email(email)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        if user.password != password:
            raise HTTPException(status_code=401, detail="Invalid credentials")

        token = await create_access_token({"sub": user.email})

        return token

    async def create_user(
        self,
        user: UserCreate,
    ):
        if not user.name:
            raise HTTPException(status_code=400, detail="Missing required properties")
        if not user.username:
            raise HTTPException(status_code=400, detail="Missing required properties")
        if not user.email:
            raise HTTPException(status_code=400, detail="Missing required properties")
        if not re.match(r"^[^\s@]+@[^\s@]+\.[^\s@]+$", user.email):
            raise HTTPException(status_code=400, detail="Email format is invalid")

        if not user.password:
            raise HTTPException(status_code=400, detail="Missing required properties")

        if await self.user_repository.exists_by_email(user.email):
            raise HTTPException(
                status_code=409, detail="Already exists a user with this email"
            )

        user_instance = User(
            id=uuid.uuid4(),
            name=user.name,
            username=user.username,
            email=user.email,
            password=hashlib.sha256(user.password.encode()).hexdigest(),
            role="customer",
        )

        return await self.user_repository.save(user_instance)

    async def delete_user(self, id: str):
        if not id:
            raise HTTPException(status_code=400, detail="Missing required properties")

        if not await self.user_repository.exists_by_id(id):
            raise HTTPException(status_code=404, detail="User not found")

        return await self.user_repository.delete_by_id(id)

    async def update_user(self, user: UserCreate):
        if not user.id:
            raise HTTPException(status_code=400, detail="Missing required properties")

        if not await self.user_repository.exists_by_id(user.id):
            raise HTTPException(status_code=404, detail="User not found")

        return await self.user_repository.save(user)
