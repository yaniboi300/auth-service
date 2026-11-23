from datetime import datetime

from uuid import UUID, uuid4
from sqlalchemy.dialects.postgresql import UUID as PGUUID
from sqlalchemy import String, DateTime, func
from sqlalchemy.orm import mapped_column, Mapped

from app.db.session import Base


class User(Base):
    __tablename__ = "users"

    id: Mapped[UUID] = mapped_column(PGUUID(as_uuid=True), primary_key=True, default=uuid4)
    email: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)
    password_hash: Mapped[str] = mapped_column(String(255), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    