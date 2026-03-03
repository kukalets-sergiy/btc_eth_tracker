from celery import shared_task
import requests


@shared_task(bind=True, autoretry_for=(requests.RequestException,), retry_backoff=True, retry_kwargs={"max_retries": 5})
def fetch_blocks_task(self):
    from app.models.block import FetchState
    from django.db import transaction

    with transaction.atomic():
        state, _ = FetchState.objects.select_for_update().get_or_create(id=1)
        next_currency = "ETH" if state.last_currency == "BTC" else "BTC"
        state.last_currency = next_currency
        state.save()
    from app.api import BlockAPI

    BlockAPI.fetch_block(next_currency)


@shared_task
def fetch_stats_task():
    from app.api import CryptoStatsAPI

    CryptoStatsAPI.fetch_stats()
