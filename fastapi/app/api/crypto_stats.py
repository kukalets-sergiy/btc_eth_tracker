import os

import logging
from django.utils.dateparse import parse_datetime

from app.models import CurrencyStats


logger = logging.getLogger(__name__)


class CryptoStatsAPI:
    SYMBOLS = ["BTC", "ETH"]

    @classmethod
    def fetch_stats(cls, api_key=os.getenv("API_KEY_COINMARKETCAP")):
        import requests
        from app.models import Currency, Provider, CurrencyStats

        provider = Provider.objects.filter(name="CoinMarketCap").first()
        if not provider:
            print("Provider not found")
            return
        url = os.getenv("URL_COINMARKETCAP")
        headers = {"X-CMC_PRO_API_KEY": api_key}
        params = {"symbol": ",".join(cls.SYMBOLS)}

        try:
            response = requests.get(url, headers=headers, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()
        except Exception as e:
            print(f"Error fetching stats: {e}")
            return

        for symbol, info in data.get("data", {}).items():
            quote = info.get("quote", {}).get("USD", {})

            currency, _ = Currency.objects.get_or_create(name=symbol)

            CurrencyStats.objects.create(
                currency=currency,
                provider=provider,
                last_updated=parse_datetime(info["last_updated"]),
                price_usd=quote["price"],
                market_cap_usd=quote["market_cap"],
                volume_24h_usd=quote["volume_24h"],
            )

    @classmethod
    def list_stats(cls, currency_name: str | None, provider_name: str | None, limit: int, offset: int):
        qs = CurrencyStats.objects.select_related("currency", "provider").all()
        if currency_name:
            qs = qs.filter(currency__name__iexact=currency_name)
        if provider_name:
            qs = qs.filter(provider__name__iexact=provider_name)
        return qs[offset : offset + limit]

    @classmethod
    def latest_stats(cls, currency_name: str, provider_name: str | None):
        qs = CurrencyStats.objects.select_related("currency", "provider").filter(currency__name__iexact=currency_name)
        if provider_name:
            qs = qs.filter(provider__name__iexact=provider_name)
        return qs.order_by("-last_updated").first()
