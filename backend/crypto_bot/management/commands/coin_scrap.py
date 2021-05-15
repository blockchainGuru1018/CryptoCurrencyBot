import io
import json
import logging  
import os
import pdb
import pprint
import psutil
import random 

from urllib.parse import urlencode

from django.core.management.base import BaseCommand, CommandError
from django.conf import settings 

import requests
from bs4 import BeautifulSoup


THIS_DIR = os.path.join(
    settings.BASE_DIR, 
    "crypto_bot", 
    "management", 
    "commands"
)


logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = 'Scrap prices from coinwatch'
    base_url = "https://coinmarketcap.com/currencies"


    def add_arguments(self, parser):
        parser.add_argument('currency', type=str)
        parser.add_argument('start_date', type=str)
        parser.add_argument('end_date', type=str)


    def handle(self, *args, **options):
        self.currency = options["currency"]
        self.start_date = options["start_date"]
        self.end_date = options["end_date"]
        self.main()


    @staticmethod
    def parse_coins(coins):
        try:
           coins = coins["props"]["initialState"]["cryptocurrency"]
           coins = coins["ohlcvHistorical"]['1']["quotes"]
        except KeyError as error:
            error = str(error)
            logger.exception(error)
            raise Exception(error) from None
        return coins 


    @staticmethod
    def get_agent():
        with io.open(os.path.join(THIS_DIR, "user_agents.txt"), "r") as ts:
            agent = random.choice(ts.readlines()).strip("\n")
        return agent


    @staticmethod
    def make_soup(chunk):
        soup = BeautifulSoup(chunk, "html.parser")
        return soup 


    def request_url(self):
        qst = urlencode({"start" : self.start_date, "end" : self.end_date})       
        url = f"{self.base_url}/{self.currency}/historical-data/?{qst}"
        return url


    def get_html(self):
        url = self.request_url()
        headers = {"user-agent" : self.get_agent()}
        response = requests.get(url, headers=headers)
        if response.status_code != 200:
            error = f"Unable to get data for url => {url}"
            logger.error(error)
            raise Exception(error) from None 
        self.stdout.write(self.style.SUCCESS(f'[!] Scrapping {url}'))
        soup = self.make_soup(response.content)
        return soup


    def coins_coins(self, coins_table):
        # scrap the coins table from the 
        data = coins_table.find(
            name="script", 
            id="__NEXT_DATA__", 
            type="application/json"
        )
        if data is None:
            error = f"[!] No data to show for {self.request_url()}"
            logger.error(error)
            raise Exception(error) from None
        load = json.loads(data.contents[0])
        return load 


    def main(self):
        try:
            scrap = self.get_html()
            coins = self.coins_coins(scrap)
            batch = self.parse_coins(coins)
        except Exception as error:
            logger.exception(str(error))
        for each in batch:
            pprint.pprint(each)
        