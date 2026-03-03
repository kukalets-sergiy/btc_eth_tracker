import os
from datetime import datetime
from django.utils import timezone
from logging import getLogger
from uuid import UUID
import requests
from app.models import Currency, Provider, Block


logger = getLogger(__name__)


BLOCKCHAIR_API = {
    "ETH": os.getenv("URL_BLOCKCHAIR"),
}

BLOCKSTREAM_API = {
    "BTC_block_height": os.getenv("BTC_BLOCK_HEIGHT"),
    "BTC_block_hash": os.getenv("BTC_BLOCK_HASH"),
    "BTC_block_info": os.getenv("BTC_BLOCK_INFO"),
}


class BlockAPI:
    @classmethod
    def fetch_block(cls, currency_name: str) -> None:
        if currency_name == "BTC":
            cls._fetch_blockstream(currency_name)
        elif currency_name == "ETH":
            cls._fetch_blockchair()
        else:
            logger.error(f"Unsupported currency: {currency_name}")

    @classmethod
    def _fetch_blockstream(cls, currency_name: str) -> None:
        try:
            block_number = int(requests.get(BLOCKSTREAM_API["BTC_block_height"], timeout=10).text)
            block_hash = requests.get(
                BLOCKSTREAM_API["BTC_block_hash"].format(block_number=block_number), timeout=10
            ).text
            block_info = requests.get(
                BLOCKSTREAM_API["BTC_block_info"].format(block_hash=block_hash), timeout=10
            ).json()
            block_time = timezone.make_aware(datetime.fromtimestamp(block_info["timestamp"]))
            cls._save_block(currency_name, "BlockStream", block_number, block_time)
        except Exception as e:
            logger.error(f"Error fetching BTC block from BlockStream: {e}")

    @classmethod
    def _fetch_blockchair(cls):
        url = BLOCKCHAIR_API["ETH"]
        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            data = response.json()["data"]
        except Exception as e:
            logger.error(f"Error fetching ETH block from BlockChair: {e}")
            return

        block_number = data["best_block_height"]
        block_time = timezone.make_aware(datetime.strptime(data["best_block_time"], "%Y-%m-%d %H:%M:%S"))

        cls._save_block("ETH", "BlockChair", block_number, block_time)

    @staticmethod
    def _save_block(currency_name: str, provider_name: str, block_number: int, block_time: datetime) -> None:
        currency, _ = Currency.objects.get_or_create(name=currency_name)
        provider, _ = Provider.objects.get_or_create(name=provider_name)

        if Block.objects.filter(currency=currency, provider=provider, block_number=block_number).exists():
            logger.info(f"Block {block_number} for {currency_name} already exists.")
            return

        Block.objects.create(
            currency=currency,
            provider=provider,
            block_number=block_number,
            created_at=block_time,
        )
        logger.info(f"Saved block {block_number} for {currency_name}")

    @classmethod
    def block_list(
        cls, currency: str | None = None, provider: str | None = None, limit: int = 20, offset: int = 0
    ) -> list[Block]:
        qs = Block.objects.select_related("currency", "provider").all()
        if currency:
            qs = qs.filter(currency__name__iexact=currency)
        if provider:
            qs = qs.filter(provider__name__iexact=provider)
        qs = qs[offset : offset + limit]
        return list(qs)

    @classmethod
    def get_block(
        cls,
        block_id: UUID | None = None,
        currency: str | None = None,
        block_number: int | None = None,
        provider: str | None = None,
    ) -> Block | None:
        qs = Block.objects.select_related("currency", "provider").order_by("-created_at")

        if block_id:
            qs = qs.filter(uuid=block_id)
        if currency:
            qs = qs.filter(currency__name__iexact=currency)
        if block_number:
            qs = qs.filter(block_number=block_number)
        if provider:
            qs = qs.filter(provider__name__iexact=provider)

        return qs.first()

    @classmethod
    def provider_list(cls) -> list["Provider"]:
        return list(Provider.objects.all())
