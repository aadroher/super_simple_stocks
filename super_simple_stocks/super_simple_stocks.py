#! /usr/bin/env python3

import enum
import abc
import operator

from datetime import datetime, timedelta
from functools import reduce

TICKER_SYMBOLS = [
    'TEA',
    'POP',
    'ALE',
    'GIN',
    'JOE'
]

TickerSymbol = enum.Enum('TickerSymbol', ' '.join(TICKER_SYMBOLS))

BUY_SELL_INDICATORS = ['BUY', 'SELL', '?']

BuySellIndicator = enum.Enum('BuySellIndicator', ' '.join(BUY_SELL_INDICATORS))


class Trade:

    def __init__(self,
                 timestamp: datetime,
                 quantity: int,
                 price_per_share: float,
                 buy_sell_indicator: BuySellIndicator):

        self.timestamp = timestamp
        self.quantity = quantity
        self.price_per_share = price_per_share
        self.buy_sell_indicator = buy_sell_indicator

    @property
    def total_price(self) -> float:
        return self.quantity * self.price_per_share


class Stock(abc.ABC):

    price_time_period = timedelta(minutes=15)

    @abc.abstractmethod
    def __init__(self,
                 symbol: TickerSymbol,
                 par_value: float):
        self.symbol = symbol
        self.par_value = par_value
        self.trades = []

    @abc.abstractmethod
    def record_trade(self, trade: Trade):
        self.trades.append(trade)

    @property
    @abc.abstractmethod
    def dividend(self) -> float:
        raise NotImplementedError

    @property
    @abc.abstractmethod
    def ticker_price(self) -> float:
        return self.trades[-1].price_per_share

    @abc.abstractmethod
    def price_earnings_ratio(self) -> float:
        return self.ticker_price / self.dividend

    @abc.abstractmethod
    def price(self) -> float:
        significant_trades = (trade for trade in self.trades
                              if trade.timestamp >= datetime.now() - self.price_time_period)
        trade_prices = (trade.total_price for trade in significant_trades)
        quantities = (trade.quantity for trade in significant_trades)
        return sum(trade_prices) / sum(quantities)


class CommonStock(Stock):

    def __init__(self,
                 symbol: TickerSymbol,
                 par_value: float,
                 last_dividend: float):

        super().__init__(symbol, par_value)
        self.last_dividend = last_dividend

    def record_trade(self, trade: Trade):
        super().record_trade(trade)

    @property
    def dividend(self):
        return self.last_dividend

    @property
    def ticker_price(self):
        return super().ticker_price

    @property
    def price_earnings_ratio(self):
        return super().price_earnings_ratio

    @property
    def price(self):
        return super().price


class PreferredStock(Stock):

    def __init__(self,
                 symbol,
                 par_value,
                 fixed_dividend):

        super().__init__(symbol, par_value)
        self.fixed_dividend = fixed_dividend

    def record_trade(self, trade: Trade):
        super().record_trade(trade)

    @property
    def dividend(self):
        return self.fixed_dividend * self.par_value

    @property
    def ticker_price(self):
        return super().ticker_price

    @property
    def price_earnings_ratio(self):
        return super().price_earnings_ratio

    @property
    def price(self):
        return super().price


class GlobalBeverageCorporationExchange:

    def __init__(self):
        self.stocks = []

    def add_stock(self, stock: Stock):
        self.stocks.append(stock)

    @property
    def all_share_index(self) -> float:
        n = len(self.stocks)
        stock_prices = (stock.price for stock in self.stocks)
        product = reduce(operator.mul, stock_prices, 1)
        return product**(1/n)

