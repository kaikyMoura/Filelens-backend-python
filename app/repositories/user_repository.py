from sqlalchemy import select
from app.models.user import User
from sqlalchemy.ext.asyncio import AsyncSession


class UserRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def find_all(self) -> list[User]:
        """
        Finds all users in the database.

        Returns:
            list[User]: A list of all users in the database.
        """
        result = await self.db.execute(select(User))
        return result.scalars().all()

    async def find_by_id(self, id: str) -> User | None:
        """
        Finds a user in the database by their id.

        Args:
            id (str): The id of the user to find.

        Returns:
            User | None: The user object if found, None otherwise.
        """
        result = await self.db.execute(select(User).filter(User.id == id))
        return result.scalars().first()

    async def find_by_email(self, email: str) -> User | None:
        """
        Finds a user in the database by their email.

        Args:
            email (str): The email of the user to find.

        Returns:
            User | None: The user with the given email, or None if no user is found.
        """
        result = await self.db.execute(select(User).filter(User.email == email))
        return result.scalars().first()

    async def save(self, user: User) -> User:
        """
        Saves a user to the database.
        Checks if a user exists in the database by their id.
        If it does, updates the user.
        Else, adds the user.

        Args:
            user (User): The user to save.

        Returns:
            User: The saved user.
        """

        self.db.add(user)
        await self.db.commit()
        await self.db.refresh(user)
        return user

    async def update(self, user: User) -> User:
        """
        Updates a user in the database.

        Args:
            user (User): The user to update.

        Returns:
            User: The updated user.
        """

        await self.db.merge(user)
        await self.db.commit()
        await self.db.refresh(user)
        return user

    async def exists_by_email(self, email: str) -> bool:
        """
        Checks if a user exists in the database by their email.

        Args:
            email (str): The email of the user to check.

        Returns:
            bool: True if a user with the given email exists, False otherwise.
        """
        result = await self.db.execute(select(User).where(User.email == email))
        return result.scalars().first() is not None

    async def exists_by_id(self, id: str) -> bool:
        """
        Checks if a user exists in the database by their id.

        Args:
            id (str): The id of the user to check.

        Returns:
            bool: True if a user with the given id exists, False otherwise.
        """
        result = await self.db.execute(select(User).filter(User.id == id))
        return result.scalars().first() is not None

    async def delete_by_id(self, id: str) -> None:
        """
        Deletes a user from the database by their id.

        Args:
            id (str): The id of the user to delete.

        Returns:
            None
        """
        result = await self.db.execute(select(User).filter(User.id == id))
        user = result.scalars().first()
        if user:
            await self.db.delete(user)
            await self.db.commit()
        else:
            raise Exception("User not found")
