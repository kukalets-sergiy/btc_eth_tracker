from pydantic import BaseModel
from datetime import datetime


class CurrencyStatsOutSchema(BaseModel):
    currency: str
    provider: str
    price_usd: float
    market_cap_usd: float
    volume_24h_usd: float
    last_updated: datetime
    stored_at: datetime
