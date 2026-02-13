from django.contrib import admin

from app.models.block import Currency, Provider, Block


@admin.register(Currency)
class CurrencyAdmin(admin.ModelAdmin):
    list_display = ("uuid", "name")
    search_fields = ("name",)


@admin.register(Provider)
class ProviderAdmin(admin.ModelAdmin):
    list_display = ("uuid", "name", "api_key")
    search_fields = ("name",)


@admin.register(Block)
class BlockAdmin(admin.ModelAdmin):
    list_display = ("uuid", "currency", "provider", "block_number", "created_at", "stored_at")
    search_fields = ("currency__name", "provider__name", "block_number")
