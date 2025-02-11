from datetime import datetime

from sqlmodel import Field, SQLModel


class RevokedToken(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    token: str = Field(index=True, unique=True)
    revoked_at: datetime = Field(default_factory=datetime.utcnow)
