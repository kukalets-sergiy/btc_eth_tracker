from logging import getLogger
from uuid import UUID

from fastapi import APIRouter, Query, HTTPException, Depends

from app.dependencies.auth import get_current_user
from app.models import User
from app.api.block import BlockAPI
from app.schemas import BlockOutSchema, ProviderOutSchema
from app.serializers import BlockSerializer
from app.serializers.block import ProviderSerializer
from app.utils.enum import ProviderEnum

logger = getLogger(__name__)

block_router = APIRouter()


@block_router.get("/blocks", response_model=list[BlockOutSchema])
def get_blocks(
    currency: str | None = Query(None),
    provider: ProviderEnum | None = Query(None),
    limit: int = Query(20, ge=1, le=100),
    offset: int = Query(0, ge=0),
    current_user: User = Depends(get_current_user),
) -> list[BlockOutSchema]:
    blocks = BlockAPI.block_list(currency, provider, limit, offset)
    serializer = BlockSerializer(blocks, many=True)
    return [BlockOutSchema.model_validate(item) for item in serializer.data]


@block_router.get("/block", response_model=BlockOutSchema)
def get_block(
    block_id: UUID | None = Query(None),
    currency: str | None = Query(None),
    block_number: int | None = Query(None),
    provider: ProviderEnum | None = Query(None),
    current_user: User = Depends(get_current_user),
) -> BlockOutSchema:
    block = BlockAPI.get_block(block_id=block_id, currency=currency, block_number=block_number, provider=provider)
    if not block:
        raise HTTPException(status_code=404, detail="Block not found")

    serializer = BlockSerializer(block)
    return BlockOutSchema.model_validate(serializer.data)


@block_router.get("/providers", response_model=list[ProviderOutSchema])
def get_providers(
    current_user: User = Depends(get_current_user),
) -> list[ProviderOutSchema]:
    providers = BlockAPI.provider_list()
    serializer = ProviderSerializer(providers, many=True)
    return [ProviderOutSchema.model_validate(item) for item in serializer.data]
