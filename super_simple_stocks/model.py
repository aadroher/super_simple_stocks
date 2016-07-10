#! /usr/bin/env python3

import enum
import abc
import operator

from datetime import datetime, timedelta
from functools import reduce


@enum.unique
class TickerSymbol(enum.Enum):
    """Unique identifier for one of the traded stocks"""
    TEA = 1
    POP = 2
    ALE = 3
    GIN = 4
    JOE = 5


@enum.unique
class BuySellIndicator(enum.Enum):
    """Indicator to buy or sell that accompanies each trade"""
    BUY = 1
    SELL = 2


class Trade:

    """A change of ownership of a collection of shares at a definite price per share"""

    def __init__(self,
                 timestamp: datetime,
                 quantity: int,
                 price_per_share: float,
                 buy_sell_indicator: BuySellIndicator):
        """
        :param timestamp: The moment when the transaction has taken place
        :param quantity: The amount of shares exchanged
        :param price_per_share: Price for each share
        :param buy_sell_indicator: Indication to buy or sell
        """

        self.timestamp = timestamp
        self.quantity = quantity
        self.price_per_share = price_per_share
        self.buy_sell_indicator = buy_sell_indicator

    @property
    def total_price(self) -> float:
        """
        :return: The total price of the trade
        """
        return self.quantity * self.price_per_share


class Stock(abc.ABC):

    """A publicly traded stock

    This is an abstract class that includes the common interface that both common
    and preferred stocks share.

    The class variable Stock.price_time_interval serves as a configuration value to
    define the length of the time interval that is significant to calculate the stock
    price.

    """

    price_time_interval = timedelta(minutes=15)

    @abc.abstractmethod
    def __init__(self,
                 symbol: TickerSymbol,
                 par_value: float):
        """
        :param symbol: The symbol that identifies this stock
        :param par_value: The face value per share for this stock
        This initializer also creates the instance variable self.trades,
        which is to hold a list of recorded instances of Trade.
        """
        self.symbol = symbol
        self.par_value = par_value

        self.trades = []

    @abc.abstractmethod
    def record_trade(self, trade: Trade):
        """
        Records a trade for this
        :param trade: The trade to be recorded
        """
        self.trades.append(trade)

    @property
    @abc.abstractmethod
    def dividend(self) -> float:
        """
        :return: A ratio that represents the dividend for this stock
        """
        pass

    @property
    @abc.abstractmethod
    def ticker_price(self) -> float:
        """
        :return: The price per share for the last recorded trade for this stock.
        """
        return self.trades[-1].price_per_share

    @property
    @abc.abstractmethod
    def dividend_yield(self) -> float:
        pass

    @property
    @abc.abstractmethod
    def price_earnings_ratio(self) -> float:
        """
        :return: The P/E ratio for this stock
        """
        return self.ticker_price / self.dividend

    @property
    @abc.abstractmethod
    def price(self) -> float:
        """
        :return: The average price per share based on trades recorded in the last
            Stock.price_time_interval.
        .. note:: Though lean, the way in which significant_trades obtained may be
            unnecessarily costly, since it traverses all recorded trades and it may
            be possible to have them already ordered by trade.timestamp.
        """
        significant_trades = (trade for trade in self.trades
                              if trade.timestamp >= datetime.now() - self.price_time_interval)
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
    def dividend_yield(self):
        return self.dividend / self.ticker_price

    @property
    def price_earnings_ratio(self):
        return super().price_earnings_ratio

    @property
    def price(self):
        return super().price


class PreferredStock(Stock):

    def __init__(self,
                 symbol: TickerSymbol,
                 par_value: float,
                 fixed_dividend: float):

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
    def dividend_yield(self):
        return (self.dividend * self.par_value) / self.ticker_price

    @property
    def price_earnings_ratio(self):
        return super().price_earnings_ratio

    @property
    def price(self):
        return super().price


class GlobalBeverageCorporationExchange:

    """The whole exchange where the trades take place"""

    def __init__(self,
                 stocks: [Stock]):
        """
        :param stocks: The stocks traded at this exchange.
        """
        self.stocks = stocks

    def record_trade(self,
                     ticker_symbol: TickerSymbol,
                     trade: Trade):
        """Records a trade for the proper stock.
        :param ticker_symbol: The identifier of the stock.
        :param trade: The trade to record.
        """
        stock = next(stock for stock in self.stocks
                     if stock.symbol == ticker_symbol)
        stock.record_trade(trade)

    @property
    def all_share_index(self) -> float:
        """The geometric mean of all stock prices"""
        n = len(self.stocks)
        stock_prices = (stock.price for stock in self.stocks)
        product = reduce(operator.mul, stock_prices, 1)
        return product**(1/n)

