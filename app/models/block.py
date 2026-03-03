from django.db import models
import uuid
from app.models.base import BaseModelMixin


class Currency(BaseModelMixin):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class Provider(BaseModelMixin):
    name = models.CharField(max_length=100, unique=True)
    api_key = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return self.name


class Block(models.Model):
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    currency = models.ForeignKey(Currency, on_delete=models.CASCADE)
    provider = models.ForeignKey(Provider, on_delete=models.SET_NULL, null=True)
    block_number = models.PositiveIntegerField()
    created_at = models.DateTimeField(verbose_name="created_at", db_index=True)
    stored_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("currency", "provider", "block_number")
        ordering = ["-created_at"]


class FetchState(models.Model):
    last_currency = models.CharField(max_length=10, default="ETH")
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Last: {self.last_currency}"
