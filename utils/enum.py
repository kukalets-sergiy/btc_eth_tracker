from enum import Enum


class ProviderEnum(str, Enum):
    BLOCKCHAIR = "Blockchair"
    BLOCKSTREAM = "BlockStream"


class StatsProviderEnum(str, Enum):
    COINMARKETCAP = "CoinMarketCap"
