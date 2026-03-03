from fastapi import APIRouter, HTTPException, Query, Depends

from app.api import CryptoStatsAPI
from app.dependencies.auth import get_current_user
from app.models import User
from app.schemas.crypto_stats import CurrencyStatsOutSchema
from app.serializers.crypto_stats import CurrencyStatsSerializer
from app.utils.enum import StatsProviderEnum

crypto_stat_router = APIRouter()


@crypto_stat_router.get("/", response_model=list[CurrencyStatsOutSchema])
def get_stats(
    currency: str | None = Query(None),
    provider: StatsProviderEnum | None = Query(None),
    limit: int = Query(20, ge=1, le=100),
    offset: int = Query(0, ge=0),
    current_user: User = Depends(get_current_user),
):
    stats = CryptoStatsAPI.list_stats(currency, provider, limit, offset)
    serializer = CurrencyStatsSerializer(stats, many=True)
    return [CurrencyStatsOutSchema.model_validate(item) for item in serializer.data]


@crypto_stat_router.get("/latest", response_model=CurrencyStatsOutSchema)
def get_latest_stats(
    currency: str = Query("BTC"),
    provider: StatsProviderEnum | None = Query(None),
    current_user: User = Depends(get_current_user),
):
    stats = CryptoStatsAPI.latest_stats(currency, provider)
    if not stats:
        raise HTTPException(status_code=404, detail="Stats not found")
    serializer = CurrencyStatsSerializer(stats)
    return CurrencyStatsOutSchema.model_validate(serializer.data)
