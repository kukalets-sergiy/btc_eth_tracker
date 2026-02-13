from rest_framework import serializers

from app.models import Block, Provider


class BlockSerializer(serializers.ModelSerializer):
    currency = serializers.CharField(source="currency.name")
    provider = serializers.CharField(source="provider.name", allow_null=True)

    class Meta:
        model = Block
        fields = [
            "uuid",
            "currency",
            "provider",
            "block_number",
            "created_at",
            "stored_at",
        ]


class ProviderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Provider
        fields = ["uuid", "name"]
