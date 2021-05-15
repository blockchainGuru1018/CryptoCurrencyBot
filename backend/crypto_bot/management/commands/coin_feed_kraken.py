import datetime
import logging 
import io 
import os
import pprint

import ccxt

from django.core.management import BaseCommand, CommandError


logger = logging.getLogger(__name__)


this_folder = os.path.dirname(os.path.abspath(__file__))
root_folder = os.path.dirname(os.path.dirname(this_folder))


class Command(BaseCommand):
    help = "Pull historical data for pair e.g BTC/USDT from kraken"
    symbols = None
    since = None
    timeframe = None 
    limit = None
    exchange = ccxt.kraken(config={})


    def add_arguments(self, parser):
        parser.add_argument(
            "symbols", 
            type=str,
            help="pair symbols XXX/XXX"
        )
        parser.add_argument(
            "--since", 
            type=str, 
            help="Date in format => yyyy-mm-dd"
        )
        parser.add_argument(
            "--timeframe",
            type=str,
            help=f"Timeframes available: {', '.join(self.exchange.timeframes)}"
        )
        parser.add_argument(
            "--limit",
            type=int,
            help="Max limit of records, max is 500 (default)"
        )


    def handle(self, **options):
        self.limit = options.get("limit", None)
        self.symbols = options.get("symbols")
        self.since = options.get("since", None)
        self.timeframe = options.get("timeframe", None)
        self.last = self.get_history()


    def make_date(self):
        try:
            if self.since is not None:
                year, month, day = [int(x) for x in self.since.split("-")]
                timestamp = (
                    datetime.datetime(
                        year=year, 
                        month=month, 
                        day=day
                    ).timestamp() / 1000)
            else:
                timestamp = None
        except Exception as error:
            logger.error(str(error))
            exit(1)
        return timestamp


    def get_history(self):
        self.stdout.write(self.style.SUCCESS(f'Feed {self.exchange.name} => {self.symbols}'))
        self.stdout.write(self.style.NOTICE("Getting a list of OHLCV candles .. "))
        
        timeframe = (
            self.timeframe if (
                self.timeframe is not None
            ) and ( 
                self.timeframe in self.exchange.timeframes
            ) 
            else '1d'
        )

        limit = (
            self.limit if (
                self.limit is not None
            ) and (
                0 > self.limit <= 500
            ) 
            else None
        )

        try:
            ohlcv = self.exchange.fetch_ohlcv(
                self.symbols,
                timeframe=timeframe,
                since=self.make_date(),
                limit=limit,
            )
        except Exception as error:
            logger.error(f"Error {str(error)} line # 100")
            exit(1)
        
        data = {
            "pair" : self.symbols, 
            "trades" : []
        }
        for each in ohlcv:
            data["trades"].append(
                {"time" : datetime.datetime.fromtimestamp(each[0]/1000),
                "open" : each[1],
                "high" : each[2],
                "low" : each[3],
                "vol" : each[4]}
            )
        # Parse the data here to insert into db or csv
        pprint.pprint(data)