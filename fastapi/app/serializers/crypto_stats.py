from rest_framework import serializers

from app.models import CurrencyStats


class CurrencyStatsSerializer(serializers.ModelSerializer):
    currency = serializers.CharField(source="currency.name")
    provider = serializers.CharField(source="provider.name")

    price_usd = serializers.FloatField()
    market_cap_usd = serializers.FloatField()
    volume_24h_usd = serializers.FloatField()

    class Meta:
        model = CurrencyStats
        fields = [
            "currency",
            "provider",
            "price_usd",
            "market_cap_usd",
            "volume_24h_usd",
            "last_updated",
            "stored_at",
        ]
