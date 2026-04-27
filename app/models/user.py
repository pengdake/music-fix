from sqlmodel import SQLModel, Field
from datetime import datetime
from sqlalchemy import Column, DateTime, func


class User(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)

    username: str = Field(index=True, unique=True)
    email: str = Field(index=True, unique=True)

    password_hash: str

    is_active: bool = Field(default=True)
    is_superuser: bool = Field(default=False)

    created_at: datetime = Field(
        sa_column=Column(DateTime(timezone=True), server_default=func.now())
    )

    updated_at: datetime = Field(
        sa_column=Column(
            DateTime(timezone=True),
            server_default=func.now(),
            onupdate=func.now()
        )
    )