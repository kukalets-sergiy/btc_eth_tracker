from datetime import datetime
from uuid import UUID
from pydantic import BaseModel, ConfigDict


class BlockOutSchema(BaseModel):
    uuid: UUID
    currency: str
    provider: str | None
    block_number: int
    created_at: datetime
    stored_at: datetime


class ProviderOutSchema(BaseModel):
    uuid: UUID
    name: str

    model_config = ConfigDict(from_attributes=True)
