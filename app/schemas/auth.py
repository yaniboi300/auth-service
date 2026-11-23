from uuid import UUID

from pydantic import BaseModel, ConfigDict, EmailStr, Field, field_validator


class UserCreate(BaseModel):
    email: EmailStr = Field(..., max_length=255, description="Email пользователя")
    password: str = Field(
        ...,
        min_length=8,
        max_length=72,
        description="Пароль (минимум 8 символов)"
    )

    @field_validator("password")
    @classmethod
    def validate_password(cls, value: str) -> str:
        if " " in value:
            raise ValueError("Пароль не должен содержать пробелов")
        if not any(char.isdigit() for char in value):
            raise ValueError("Пароль должен содержать хотя бы одну цифру")
        return value


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"


class UserResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    email: EmailStr
