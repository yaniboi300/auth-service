from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models import User


class AuthRepository:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def create_user(self, user: User) -> User:
        self.session.add(user)
        await self.session.flush()
        await self.session.refresh(user)
        return user

    async def get_user_by_email(self, email: str) -> User | None:
        query = select(User).where(User.email == email)
        return await self.session.scalar(query)

    async def get_user_by_id(self, user_id: int) -> User | None:
        query = select(User).where(User.id == user_id)
        return await self.session.scalar(query)