from django.db import models

from app.models.base import BaseModelMixin


class CurrencyStats(BaseModelMixin):
    currency = models.ForeignKey("Currency", on_delete=models.CASCADE)
    provider = models.ForeignKey("Provider", on_delete=models.CASCADE)
    price_usd = models.DecimalField(max_digits=20, decimal_places=8, null=True)
    market_cap_usd = models.DecimalField(max_digits=25, decimal_places=2, null=True)
    volume_24h_usd = models.DecimalField(max_digits=25, decimal_places=2, null=True)
    last_updated = models.DateTimeField(null=True)
    stored_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-stored_at"]
