from enum import Enum

BTCAmount = float
FiatAmount = float


class CurrencyPair(Enum):
    BTC_USD = "BTC/USD"
    BTC_EUR = "BTC/EUR"

    BCH_USD = "BCH/USD"
    BCH_EUR = "BCH/EUR"

    ETH_USD = "ETH/USD"
    ETH_EUR = "ETH/EUR"

    BNB_BTC = "BNB/BTC"
    ADA_BNB = "ADA/BNB"
    ADA_BTC = "ADA/BTC"

    ANT_BNB = "ANT/BNB"
    ANT_BTC = "ANT/BTS"

    ATOM_BNB = "ATOM/BNB"
    ATON_BTC = "ATOM/BTC"

    AVA_BNB = "AVA/BNB"
    AVA_BTC = "AVA/BTC"

    AVAX_BNB = "AVAX/BNB"
    AVAX_BTC = "AVAX/BTC"

    @property
    def fiat_symbol(self):
        if self in [CurrencyPair.BTC_EUR, CurrencyPair.BCH_EUR, CurrencyPair.ETH_EUR]:
            return '€'
        elif self in [CurrencyPair.BTC_USD, CurrencyPair.BCH_USD, CurrencyPair.ETH_USD]:
            return '$'
        else:
            return 'B'
