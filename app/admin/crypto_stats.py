from django.contrib import admin
from app.models import CurrencyStats


@admin.register(CurrencyStats)
class CurrencyStatsAdmin(admin.ModelAdmin):
    list_display = (
        "currency",
        "provider",
        "price_usd",
        "market_cap_usd",
        "volume_24h_usd",
        "last_updated",
        "stored_at",
    )
    list_filter = ("currency", "provider")
    search_fields = ("currency__name", "provider__name")
    ordering = ("-stored_at",)
