import os ,sys
import pprint
from django.conf import settings
import django
from django.core.management import BaseCommand, CommandError
main_folder = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(main_folder)
import ccxt 
from services.ccxt_api import CCXTApiHandler as handler
from services.coingecko import CoinGeckoHandler as gecko_handler
print(main_folder)

from models import *

class Command(BaseCommand):
    exchanges = [
        "Binance",
        "Kraken",
        "Bisq",
        "coinbase",
        'bitfinex',
        'kucoin',
        'ftx',
        'liquid',
        'bithumb',
        'poloniex',
    ]

    obj_handler = handler()

    def add_arguments(self, parser):
        parser.add_argument(
            "--list-exchanges",
            help="List exchanges available."
        )
        parser.add_argument(
            "--list-trade-pairs",
            help="List trade pairs for a given exchange."
        )
        parser.add_argument(
            "--exchange",
            type=str,
            help="Exchange ID (run command with --list-exchanges option)."
        )

        parser.add_argument(
            "--list_exchange_trade_pair_ohlcv",
            help="List the ohlcv values for the given trade and exchange."
        )
        parser.add_argument(
            "--exchange",
            type=str,
            help="Exchange ID (run command with --list_exchange_trade_pair_ohlcv option)."
        )


        parser.add_argument(
            "--traid-pair",
            type=str,
            help="Trade pair identifier of the exchange (run command with --list_exchange_trade_pair_ohlcv option)."
        )
        parser.add_argument(
            "--since",
            type=int,
            help="timestamp to start looking from (run command with --list_exchange_trade_pair_ohlcv option)."
        )
        parser.add_argument(
            "--limit",
            type=int,
            help="timestamp to stop looking to (run command with --list_exchange_trade_pair_ohlcv option)."
        )
        parser.add_argument(
            "--granularity",
            type=str,
            help="specification between records (run command with --list_exchange_trade_pair_ohlcv option)."
        )
        parser.add_argument(
            "--commit",
            type=bool,
            help="save the data in the db (run command with --list_exchange_trade_pair_ohlcv option)."
        )

        parser.add_argument(
            "--cache",
            type=bool,
            help="print the data in the terminal (run command with --list_exchange_trade_pair_ohlcv option)."
        )

    def handle(self, **options):
        if options.get("list_exchanges", None) is not None:
            self.list_exchanges()
            exit(0)
        if options.get("list_trade_pairs", None) is not None and options.get("exchange", None) is not None:
            exchange = options.get("exchange")
            self.list_trade_pairs_by_exchange(exchange)
            exit(0)
        if options.get('list_exchange_trade_pair_ohlcv',None) and (options.get("exchange", None)
                                 and
                                options.get("trade_pair", None)
                                and
                                options.get("since", None)
                                and
                                options.get("limit", None)
                                and
                                options.get("granularity", None)
                               and
                               (options.get("commit", None) or options.get("cache", None))
                                 ):
            params = {key:value for key, value in options.items() if key in ["exchange","trade_pair",
                                                                             "since","limit","granularity",'cache',
                                                                             'commit']}
            self.list_exchange_trade_pair_ohlcv(params=params)
            exit(0)


    def list_exchanges(self):
        self.stdout.write(self.style.SUCCESS("Listing available exchanges"))
        self.stdout.write(self.style.WARNING("---------------------------"))
        for exchange in self.exchanges:
            self.stdout.write(exchange)

    def list_trade_pairs_by_exchange(self, exchange):
        try:
            exchange = getattr(ccxt, exchange.lower())()
            markets = exchange.load_markets().keys()
        except Exception as error:
            self.stdout.write(self.style.ERROR(str(error)))
            return False
        for market in markets:
            self.stdout.write(self.style.WARNING(market))
        return True

    # this one is set up to work with coingecko
    def list_general_trade_pair_ohlcv(self, coin_id, currency, from_timestamp, to_timestamp):
        """
        gets the coin data coming from the
        given data which comes with the
        ohlcv values for the given coin
        The command 1.2 --list_general_trade_pair_ohlcv requires changes.

        We use pycoingecko.CoinGeckoAPI().t1.get_coin_market_chart_range_by_id(id='bitcoin', vs_currency='eur', from_timestamp='1562338218', to_timestamp='1563153464')
        to retrieve price (i.e. set ohlc=price, just 4 redundant fields that have the same value), volume, market_cap (this one will be omitted for now,
        it won't be printed, nor stored in the DB). Each property has a separate timestamp. We need to resample values, so that we take a union of timestamps,
        interpolate using nearest.

        Granularity doesn't make sense here, let's make it --granularity <auto>. If none has been specified, a default value is 'auto', otherwise anything like
        <1m/1h/1d> will trigger an error, that forces to specify either 'auto' or omit the flag.
        pycoingecko.CoinGeckoAPI().get_coin_ohlc_by_id(id='bitcoin', vs_currency='eur', days='max') is worse. It provides sparse timestamps, and doesn't support ranges.
        The command should provide a general information on a trade pair. It must unify information across exchanges. It should not depend on exchange parameter.
        Ideally, we would be using an average across exchanges, or pick up the most trusted. We make coingecko responsible for this task, and just take their data.

        :param trade_pair:
        :param since:
        :param limit:
        :param timeframe:
        :return:
        """

    def list_exchange_trade_pair_ohlcv(self, params):
        """
        lists the ohlcv for the given exchange with the given filters
        :param params: dict containing:
            :param trade_pair: identification for the exhange
            :param since: time to start fetching
            :param limit: time to stop fetching from
            :param granularity: how long the difference is between records
        :return:json
        """
        accepted_params =  ["exchange", "trade_pair", "since","limit","granularity",'commit','cache']
        if not all(value for key ,value in params.items() if key in accepted_params):
            self.stderr.write(self.style.ERROR("there's an issue with the parameters provided, try again."))
            return False
        try:
            exchange = handler.load_exchange_manager(exchange=params['exchange'])
            data = handler.list_ohlcvs(exchange_obj=exchange,symbol=params['trade_paid'], since=params['since'],
                                         limit=params['limit'], timeframe=params['granularity'])
            for obj_ohlcv in data:
                if params['cache']:
                    self.stdout.write(self.style.WARNING(obj_ohlcv))
                elif params['commit']:
                    obj = Exchange.get_obj(search_key=params['exchange']) if Exchange.exists(params['exchange'])\
                        else Exchange.objects.create(dump_data=handler.get_exchange_fields(exchange))

                    obj.ohlcv_set.create(
                        timestamp=obj_ohlcv.timestamp,
                        open_price=obj_ohlcv.o,
                        highest_price=obj_ohlcv.h,
                        lowest_price=obj_ohlcv.l,
                        closing_price=obj_ohlcv.c,
                        volume=obj_ohlcv.v,
                    )
            return True

        except Exception as X:
            self.stderr.write(self.style.ERROR(f"there's an issue with the request {X}, try again."))
            return False
