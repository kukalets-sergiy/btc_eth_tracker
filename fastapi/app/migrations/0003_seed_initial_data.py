from django.db import migrations


def seed_data(apps, schema_editor):
    Currency = apps.get_model("app", "Currency")
    Provider = apps.get_model("app", "Provider")

    Currency.objects.get_or_create(name="ETH")
    Currency.objects.get_or_create(name="BTC")

    Provider.objects.get_or_create(name="BlockChair")
    Provider.objects.get_or_create(name="BlockStream")
    Provider.objects.get_or_create(name="CoinMarketCap")


class Migration(migrations.Migration):

    dependencies = [
        ("app", "0002_currency_fetchstate_provider_currencystats_block"),
    ]

    operations = [
        migrations.RunPython(seed_data),
    ]
