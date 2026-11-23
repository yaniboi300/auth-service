
from sqlalchemy.exc import IntegrityError

from app.models import User
from app.repositories.auth import AuthRepository
from app.core.config import Settings
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.security import create_access_token, get_password_hash, verify_password
from app.core.exceptions import ConflictError, UnauthorizedError

class AuthService:

    def __init__(self, session: AsyncSession, settings: Settings) -> None:
        self.session = session
        self.settings = settings
        self.auth = AuthRepository(session)


    async def register_user(self, *, email: str, password: str) -> User:

        existing_user = await self.auth.get_user_by_email(email)
        if existing_user:
            raise ConflictError("User with this email already exists")

        user = User(email=str(email), password_hash=get_password_hash(password))
        try:
            await self.auth.create_user(user)
            await self.session.commit()
        except IntegrityError as exc:
            # The unique constraint is the final protection against two
            # simultaneous registrations with the same email.
            await self.session.rollback()
            raise ConflictError("User with this email already exists") from exc
        return user

    async def login_user(self, *, email: str, password: str) -> tuple[User, str]:

        user = await self.auth.get_user_by_email(email)

        if user is None or not verify_password(password, user.password_hash):
            raise UnauthorizedError("Invalid email or password")
        
        token = create_access_token(subject=str(user.id), settings=self.settings)

        return user, token
        
        
    

