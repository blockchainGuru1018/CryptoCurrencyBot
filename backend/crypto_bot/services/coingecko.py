import json
import requests as rq
import pycoingecko as coingecko



class CoinGeckoHandler(object):
    """
    Coin gecko handler
    which is only an implementation of
    the public API coingecko with the
    pythond sdk.
    """
    def __init__(self):
        self.coin_manager = self.load_manager()
        self.supported_currencies = self.load_supported_currencies()

    def load_supported_currencies(self):
        """
        loads all supported currencies for
        coingecko
        :return: list
        """
        return self.coin_manager.get_supported_vs_currencies()

    def load_manager(self):
        """
        Creates a general object
        to process all requests through
        the SDK
        :return:coin Object
        """
        return coingecko.CoinGeckoAPI()

    def list_coins(self):
        """
        lists all coins supported by
        coingecko
        :return: dict
        """
        return self.coin_manager.get_coins()

    def get_coins_prices(self,ids,currencies):
        """
        loads the current prices for the given coins
        in the based currenies
        :param ids:  list of str containing the ids of each coin
        :param currencies: list of str of the currencies to get the prices on : usd, etc.
        :return: list
        """
        return self.coin_manager.get_price(ids,currencies)

    def list_coin_markets(self, currency):
        """
        lists all of the details for the markets
        for all available coins
        :param currency: str: identifier of the currency
        e.g. : usd
        :return: list of dict
        """
        return self.coin_manager.get_coins_markets(vs_currency=currency)

    def get_coin_details(self,coin_id):
        """
        gets the details for the given coin
        :param coin_id: str
        :return: dict
        """
        return self.coin_manager.get_coin_by_id(coin_id)

    def get_coin_history(self, coin_id, date):
        """
        gets the market histroy for the coin given
        :param coin_id: str
        :param date: date : date to get the history from
        :return: list
        """
        return self.coin_manager.get_coin_history_by_id(coin_id, date)

    def get_coin_tickets(self,coin_id):
        """
        gets the tickets issued to the coins
        :param coin_id: str
        :return: list
        """
        return self.coin_manager.get_coin_ticker_by_id(coin_id)

    def get_coin_status_updates_by_id(self,coin_id):
        """
        loads the status updates based by id
        basically the status comes from the
        :param coin_id: str
        :return: dict
        """
        return self.coin_manager.get_coin_status_updates_by_id(coin_id)

    def get_coin_market_chart(self, coin_id, currency,days_up_to):
        """
        Get historical market data include price,
        market cap, and 24h volume (granularity auto)
        Minutely data will be used for duration within 1 day,
        Hourly data will be used for duration between 1 day and 90 days,
        Daily data will be used for duration above 90 days
        :param coin_id:
        :param currency: str: identifier of the currency: e.g: usd
        :param days_up_to: int: number of days to get the data from
        :return: list
        """
        return self.coin_manager.get_coin_market_chart_by_id(coin_id, currency, days_up_to)

    def get_coin_market_date_range(self, coin_id, currency, date_from, date_to):
        """
        Get historical market data include price,
        market cap, and 24h volume within a range of timestamp (granularity auto)
        Minutely data will be used for duration within 1 day,
        Hourly data will be used for duration between 1 day and 90 days,
        Daily data will be used for duration above 90 days.
        :param coin_id:str
        :param currency: str: identifier of the currency: e.g: usd
        :param date_from: timestamp: timestamp to start mapping from
        :param date_to: timestamp: timestamp to stop mapping to
        :return: list
        """
        return self.coin_manager.get_coin_market_chart_range_by_id(coin_id, currency, date_from, date_to)

    # Exchanges
    def get_exchanges(self):
        """
        gets all available exchanges
        for the available currencies existing in the moment.
        :return: list
        """
        return self.coin_manager.get_exchange_rates()

    def get_all_exchange_rates(self):
        """
        lists all exchange rates
        required for the convertion or trading
        :return: list
        """
        return self.coin_manager.get_exchange_rates()

    def get_exchange_detail(self,exchange_id):
        """
        gets all details and top 100 tickets
        for the exchange provided.
        :param exchange_id: str
        :return: dict
        """
        return self.coin_manager.get_exchanges_by_id(exchange_id)

    def get_exchange_status_update(self,exchange_id):
        """
        returns the update status on the given exchange
        :param exchange_id: str
        :return: dict
        """
        return self.coin_manager.get_exchanges_status_updates_by_id(exchange_id)

    def get_exchange_volume_chart(self,exchange_id):
        """
        Get volume_chart data for a given exchange
        :param exchange_id: str
        :return: dict
        """
        return self.coin_manager.get_exchanges_volume_chart_by_id(exchange_id)

    # finance
    def get_all_finances_markets(self):
        """
        lists all of the finance markets available
        :return: list
        """
        return self.coin_manager.get_finance_platforms()

    def get_all_finances_products(self):
        """
        lists all of the finance products available
        :return: list
        """
        return self.coin_manager.get_finance_products()

    # contract

    def get_coin_contract(self,coin_id,contract_address):
        """
        Get coin info from contract address
        :param coin_id: str coin id
        :param contract_address: str token for the address of the contract
        :return: dict
        """
        return self.coin_manager.get_coin_info_from_contract_address_by_id(coin_id, contract_address)

    def get_coin_contract_historical_chart(self, coin_id, contract_address,currency,days):
        """
        Get historical market data include price, market cap, and 24h volume (granularity auto)

        :param coin_id: str
        :param contract_address: str
        :param currency:  str
        :param days: str
        :return: list
        """
        return self.coin_manager.get_coin_market_chart_from_contract_address_by_id(coin_id,
                                                                                   contract_address,currency,days)

    def get_coin_contract_historical_range(self,coin_id, contract_address, currency, date_from, date_to):
        """
        Get historical market data include price, market cap,
        and 24h volume within a range of timestamp (granularity auto)

        :param coin_id:str
        :param contract_address: str
        :param currency: str: identifier of the currency: e.g: usd
        :param date_from: timestamp: timestamp to start mapping from
        :param date_to: timestamp: timestamp to stop mapping to
        :return: list
        """
        return self.coin_manager.get_coin_market_chart_range_from_contract_address_by_id(coin_id,
                                                                                         contract_address,
                                                                                         currency, date_from, date_to)

    def get_exchanges_global_data(self):
        """
        gets all global data to the exchanges
        :return: list
        """
        return self.coin_manager.get_global()