from django.db import models
import json

EXCHANGES = [
    ('plx', 'ploniex'),
    ('kr', 'kraken'),
    ('btx', 'bittrex'),
    ('gdx', 'gdax'),
    ('bn', 'binance'),
    ('cry', 'cryptoia'),
    ('bit', 'bitfinex'),
    ('kc', 'kucoin'),
    ('cx', 'cexio'),
    ('hi', 'htbtc'),
]


class BaseModel(models.Model):
    class Meta:
        abstract = True

    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"API Object: {self}"


class Hooper(BaseModel):
    exchange = models.CharField(max_length=10, choices=EXCHANGES, default=EXCHANGES[4])
    base_currency = models.CharField(max_length=100)
    name = models.CharField(max_length=200)
    buying_enabled = models.IntegerField()
    start_balance = models.FloatField()
    enabled = models.BooleanField(default=True)
    selling_enabled = models.BooleanField(default=False)


class HooperConfiguration(BaseModel):
    strategies = [
        ('N', 'none'),
        ('bba', 'bbands_easy'),
        ('rsi', 'rsi'),
        ('fr', 'fixed_rates'),
    ]
    tickets = [
        ('hga', 'highest_bid_lowest_ask'),
        ('ltl', 'last_tick_if_higher_lower'),
        ('alt', 'always_last_tick'),
    ]
    hooper = models.ForeignKey(Hooper, on_delete=models.CASCADE)
    exchange = models.CharField(max_length=10, choices=EXCHANGES, default=EXCHANGES[4])
    base_currency = models.CharField(max_length=10)
    selected_coins = models.CharField(max_length=10)
    strategy = models.CharField(max_length=10, choices=strategies, default=strategies[0])
    sell_with_strategy = models.IntegerField()
    targets_to_buy = models.IntegerField()
    pct_profit = models.IntegerField()
    ticket_rate = models.CharField(max_length=5, choices=tickets, default=tickets[0])
    cool_down = models.IntegerField()
    one_open_order_coin = models.IntegerField()
    pct_lower_bid = models.IntegerField()
    pct_higher_ask = models.IntegerField()
    stop_loss_pct = models.IntegerField()
    trailing_stop_loss = models.IntegerField()
    trailing_stop_loss_pct = models.IntegerField()


class HopperPool(BaseModel):
    hopper_config = models.ForeignKey(HooperConfiguration, on_delete=models.CASCADE)
    pool_name = models.CharField(max_length=100)
    exchange = models.CharField(max_length=10, choices=EXCHANGES, default=EXCHANGES[4])
    base_currency = models.CharField(max_length=10)
    selected_coins = models.CharField(max_length=10)
    enabled = models.IntegerField()


class HopperTemplate(BaseModel):
    hooper = models.ForeignKey(Hooper, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=100)


class HooperPosition(BaseModel):
    hooper = models.ForeignKey(Hooper, on_delete=models.CASCADE)
    take_profit = models.IntegerField()
    stop_loss = models.IntegerField()
    stop_loss_percentage = models.IntegerField()
    trailing_stop_loss = models.IntegerField()
    trailing_stop_loss_percentage = models.FloatField()
    trailing_stop_loss_arm = models.IntegerField()
    auto_close = models.IntegerField()
    auto_close_time = models.IntegerField()


class Order(BaseModel):
    hooper = models.ForeignKey(Hooper, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    coin = models.CharField(max_length=10)
    amount = models.IntegerField()
    price = models.FloatField()
    market_order = models.IntegerField()
    trailing_buy = models.IntegerField()
    trailing_by_pct = models.IntegerField()
    pct_profit = models.IntegerField()


class OrderStatus(BaseModel):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    timestamp = models.IntegerField()
    status = models.CharField(max_length=100)


class Strategy(BaseModel):
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=100)
    image = models.CharField(max_length=100)
    min_buys = models.IntegerField()
    min_sells = models.IntegerField()


class StrategyConfiguration(BaseModel):
    strategy = models.ForeignKey(Strategy, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    chartperiod = models.CharField(max_length=100)
    params = models.CharField(max_length=100)
    config_type = models.CharField(max_length=100)
    description = models.CharField(max_length=100)
    signal_when = models.CharField(max_length=100)
    signal_when_value = models.CharField(max_length=100)
    candle_value = models.CharField(max_length=100)
    candle_pattern = models.CharField(max_length=100)
    keep_signal = models.CharField(max_length=100)

class DataHistory(BaseModel):
    """
    Model directly created in order
    to save the data coming from
    the scrapper from the different
    sources.
    """
    currency = models.CharField(max_length=100)
    time_open = models.DateField()
    time_close = models.DateField()
    time_high = models.DateField()
    time_low = models.DateField()
    open = models.DecimalField(decimal_places=10, max_digits=255)
    high = models.DecimalField(decimal_places=10, max_digits=255)
    low = models.DecimalField(decimal_places=10, max_digits=255)
    close = models.DecimalField(decimal_places=10, max_digits=255)
    volume = models.DecimalField(decimal_places=10, max_digits=255)
    market_cap = models.DecimalField(decimal_places=10, max_digits=255)


# ~+~+~+~+~+~+~+~+~+~+~+~+~+~+~+~+~+~+~+~+~+~+~+~+~+~+~+~+~+~+~+~+~+~+~+~+~+
# cctx models for the feed.
# ~+~+~+~+~+~+~+~+~+~+~+~+~+~+~+~+~+~+~+~+~+~+~+~+~+~+~+~+~+~+~+~+~+~+~+~+~+


# class Exchange(BaseModel):
#     exchange_id = models.CharField(max_length=20)
#     name = models.CharField(max_length=100)
#
#
# class ExchangeCountriesSupported(BaseModel):
#     exchange = models.ForeignKey(Exchange,on_delete=models.CASCADE)
#     country = models.CharField(max_length=100)

    
class Market(BaseModel):
    market_id = models.CharField(max_length=20)
    symbol = models.CharField(max_length=20)
    base = models.CharField(max_length=20)
    base_id = models.CharField(max_length=20)
    quote_id = models.CharField(max_length=20)
    active = models.BooleanField()
    taker = models.DecimalField(decimal_places=10,max_digits=255)
    maker = models.DecimalField(decimal_places=10,max_digits=255)
    percentage = models.BooleanField()
    info = models.TextField()

    
class MarketPrecision(BaseModel):
    market = models.ForeignKey(Market,on_delete=models.CASCADE)
    price = models.IntegerField(blank=True)
    amount = models.IntegerField(blank=True)
    cost = models.IntegerField(blank=True)

    
class MarketLimits(BaseModel):
    market = models.ForeignKey(Market,on_delete=models.CASCADE)
    min_amount = models.DecimalField(decimal_places=5, max_digits=20)
    max_amount = models.DecimalField(decimal_places=5, max_digits=20)

    
class MarketPrice(BaseModel):
    market = models.ForeignKey(Market,on_delete=models.CASCADE)
    min_amount = models.DecimalField(decimal_places=5, max_digits=20)
    max_amount = models.DecimalField(decimal_places=5, max_digits=20)

    
class MarketCost(BaseModel):
    market = models.ForeignKey(Market,on_delete=models.CASCADE)
    min_amount = models.DecimalField(decimal_places=5, max_digits=20)
    max_amount = models.DecimalField(decimal_places=5, max_digits=20)

    
class Currency(BaseModel):
    currency_id = models.CharField(max_length=20)
    code = models.CharField(max_length=20)
    name = models.CharField(max_length=200)
    active = models.BooleanField()
    fee = models.FloatField()
    precision = models.DecimalField(decimal_places=10,max_digits=255)

    
class CurrencyLimits(BaseModel):
    currency = models.ForeignKey(Currency,on_delete=models.CASCADE)
    min_amount = models.DecimalField(decimal_places=5, max_digits=20)
    max_amount = models.DecimalField(decimal_places=5, max_digits=20)

    
class CurrencyPrice(BaseModel):
    currency = models.ForeignKey(Currency,on_delete=models.CASCADE)
    min_amount = models.DecimalField(decimal_places=5, max_digits=20)
    max_amount = models.DecimalField(decimal_places=5, max_digits=20)

    
class CurrencyCost(BaseModel):
    currency = models.ForeignKey(Currency,on_delete=models.CASCADE)
    min_amount = models.DecimalField(decimal_places=5, max_digits=20)
    max_amount = models.DecimalField(decimal_places=5, max_digits=20)

    
class CurrencyWithdrawal(BaseModel):
    currency = models.ForeignKey(Currency,on_delete=models.CASCADE)
    min_amount = models.DecimalField(decimal_places=5, max_digits=20)
    max_amount = models.DecimalField(decimal_places=5, max_digits=20)


class Ticket(BaseModel):
    symbol = models.CharField(max_length=200)
    info = models.CharField(max_length=200)
    timestamp = models.IntegerField()
    datetime = models.DateTimeField()
    high = models.DecimalField(decimal_places=10,max_digits=200)
    low = models.DecimalField(decimal_places=10,max_digits=200)
    bid = models.DecimalField(decimal_places=10,max_digits=200)
    bid_volume = models.DecimalField(decimal_places=10,max_digits=200)
    ask = models.DecimalField(decimal_places=10,max_digits=200)
    ask_volume = models.DecimalField(decimal_places=10,max_digits=200)
    vwap = models.DecimalField(decimal_places=10,max_digits=200)
    open = models.DecimalField(decimal_places=10,max_digits=200)
    close = models.DecimalField(decimal_places=10,max_digits=200)
    last = models.DecimalField(decimal_places=10,max_digits=200)
    previous_close = models.DecimalField(decimal_places=10,max_digits=200)
    change = models.DecimalField(decimal_places=10,max_digits=200)
    percentage = models.DecimalField(decimal_places=10,max_digits=200)
    average = models.DecimalField(decimal_places=10,max_digits=200)
    base_volume = models.DecimalField(decimal_places=10,max_digits=200)
    quote_volume = models.DecimalField(decimal_places=10,max_digits=200)


class BaseFetchedDataModel(BaseModel):
    """
       for the moment this will hold
       the data for the models since
       we haven't identified which fields
       to save and which to discard.
       """
    dump_data = models.TextField()

    class Meta:
        abstract = True


    def __repr__(self):
        return f"<BaseGenericDataModel:CreatedAt:{self.created_at}>"

    def format_data(self):
        """
        returns a python obj
        so that the data could be accessible easier
        :return: dict
        """
        return json.loads(self.dump_data) if self.dump_data else None

    @property
    def data_obj(self):
        """
        gets the json data and loads it
        in a dictionary
        :return: dict
        """
        return self.format_data()

    def load_attrb(self):
        """
        helps to load the attributes for managing
        the data better
        :return: self
        """
        data = self.format_data()
        for key in data.keys():
            self.__setattr__(key,data[key])
        return self

    def save(self, *args,**kwargs):
        """
        modifies the basic save method
        by removing those attributes which have no
        part in the table
        :param force_insert:
        :param force_update:
        :param using:
        :param update_fields:
        :return: object instance
        """
        self.reprocess_data()
        return super().save(args,kwargs)

    def reprocess_data(self):
        """
        adds all of the data required to the
        json data to be saved.
        :return: None
        """
        data = self.data_obj
        if data:
            for key in self.__dict__.keys():
                if key in data.keys():
                    data[key] = self.__getattribute__(key)
            self.dump_data = data


class Coin(BaseFetchedDataModel):

    def __repr__(self):
        return f"<CoinObj:CreatedAt:{self.created_at}>"


class Exchange(BaseFetchedDataModel):

    def __repr__(self):
        return f"<ExchangeObj:CreatedAt:{self.created_at}>"

    @staticmethod
    def get_obj(exchange_name):
        """
        returns the exchange object
        :param exchange_name: str
        :return: obj
        """
        data = Exchange.objects.all()
        for obj in data:
            if obj.load_data()['name'] == exchange_name:
                return obj
    @staticmethod
    def exists(exchange_name):
        """
        verifies if the given exchange existis in the db
        :param exchange_name: str
        :return: bool
        """
        result = False
        data = Exchange.objects.all()
        for obj in data:
            if obj.load_data()['name'] == exchange_name:
                result = True
                break
        return result

class OHLCV(BaseModel):
    exchange = models.ForeignKey(Exchange,on_delete=models.CASCADE)
    timestamp = models.IntegerField()
    open_price = models.DecimalField(decimal_places=10, max_digits=200)
    highest_price = models.DecimalField(decimal_places=10, max_digits=200)
    lowest_price = models.DecimalField(decimal_places=10, max_digits=200)
    closing_price = models.DecimalField(decimal_places=10, max_digits=200)
    volume = models.DecimalField(decimal_places=10, max_digits=200)

    @property
    def o(self):
        return self.open_price

    @property
    def h(self):
        return self.highest_price

    @property
    def l(self):
        return self.lowest_price

    @property
    def c(self):
        return self.closing_price

    @property
    def v(self):
        return self.volume


      
class CoinHistoricalData(BaseFetchedDataModel):
    coin = models.ForeignKey(Coin,on_delete=models.CASCADE)

    def __repr__(self):
        return f"<CoinDataHistory:CreatedAt:{self.created_at}>"


class Contract(BaseFetchedDataModel):
    coin = models.ForeignKey(Coin,on_delete=models.CASCADE)

    def __repr__(self):
        return f"<ContractObject:CreatedAt:{self.created_at}>"


class Trade(BaseFetchedDataModel):

    def __repr__(self):
        return f"<TradeObject:CreatedAt:{self.created_at}>"