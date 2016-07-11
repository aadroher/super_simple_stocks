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
                 ticker_symbol: TickerSymbol,
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

        self.ticker_symbol = ticker_symbol
        self.timestamp = timestamp

        if quantity > 0:
            self.quantity = quantity
        else:
            msg = "The quantity of shares has to be positive."
            raise ValueError(msg)

        if price_per_share >= 0.0:
            self.price_per_share = price_per_share
        else:
            msg = "The price per share can not be negative."
            raise ValueError(msg)

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

    .. note:: The class variable Stock.price_time_interval serves as a configuration value to
        define the length of the time interval that is significant to calculate the stock
        price.
    """

    price_time_interval = timedelta(minutes=15)

    def __init__(self,
                 ticker_symbol: TickerSymbol,
                 par_value: float):
        """
        :param ticker_symbol: The ticker_symbol that identifies this stock
        :param par_value: The face value per share for this stock
        .. note:: This initializer also creates the instance variable self.trades,
            which is to hold a list of recorded instances of Trade.
        """
        self.ticker_symbol = ticker_symbol
        self.par_value = par_value

        self.trades = []

    def record_trade(self, trade: Trade):
        """Records a trade for this stock.
        :param trade: The trade to be recorded
        :raise TypeError:
        :raise ValueError:
        """
        if not isinstance(trade, Trade):
            msg = "Argument trade={trade} should be of type Trade.".format(trade=trade)
            raise TypeError(msg)
        elif self.ticker_symbol is not trade.ticker_symbol:
            msg = "Argument trade={trade} does not belong to this stock.".format(trade=trade)
            raise ValueError(msg)
        else:
            self.trades.append(trade)

    @property
    @abc.abstractmethod
    def dividend(self) -> float:
        """
        :return: A ratio that represents the dividend for this stock
        """
        pass

    @property
    def ticker_price(self) -> float:
        """
        :return: The price per share for the last recorded trade for this stock
        :raise AttributeError:
        .. note:: We don't know if the trades will be registered in chronological order.
            That is why self.trades is explicitly sorted.
        """
        if len(self.trades) > 0:
            by_timestamp = sorted(self.trades,
                                  key=lambda trade: trade.timestamp,
                                  reverse=True)
            return by_timestamp[0].price_per_share
        else:
            msg = "The last ticker price is not yet available."
            raise AttributeError(msg)

    @property
    def dividend_yield(self) -> float:
        return self.dividend / self.ticker_price

    @property
    def price_earnings_ratio(self) -> float:
        """
        :return: The P/E ratio for this stock
        """
        if self.dividend != 0:
            return self.ticker_price / self.dividend
        else:
            return None

    def price(self,
              current_time: datetime=datetime.now()) -> float:
        """
        :param current_time: The point of time defined as the current one.
        :return: The average price per share based on trades recorded in the last
            Stock.price_time_interval. None if there are 0 trades that satisfy this
            condition.
        .. note:: Though lean, the way in which significant_trades obtained may be
            unnecessarily costly, since it traverses all recorded trades and it may
            be possible to have them already ordered by trade.timestamp.
        .. note:: The existence of the current_time parameter avoids the inner user
            of datetime.now, thus keeping referential transparency and moving state out.
        """
        significant_trades = [trade for trade in self.trades
                              if trade.timestamp >= current_time - self.price_time_interval]

        if len(significant_trades) > 0:
            trade_prices = (trade.total_price for trade in significant_trades)
            quantities = (trade.quantity for trade in significant_trades)
            return sum(trade_prices) / sum(quantities)
        else:
            return None



class CommonStock(Stock):

    """A common stock"""

    def __init__(self,
                 ticker_symbol: TickerSymbol,
                 par_value: float,
                 last_dividend: float):
        """
        :param last_dividend: An absolute value that indicates the last dividend
            per share for this stock.
        """

        super().__init__(ticker_symbol, par_value)
        self.last_dividend = last_dividend

    @property
    def dividend(self):
        return self.last_dividend


class PreferredStock(Stock):

    """A preferred stock"""

    def __init__(self,
                 ticker_symbol: TickerSymbol,
                 par_value: float,
                 fixed_dividend: float):
        """
        :param fixed_dividend: A decimal number that expresses the fixed dividend
            as a ratio of the face value of each share.
        """

        super().__init__(ticker_symbol, par_value)
        self.fixed_dividend = fixed_dividend

    @property
    def dividend(self):
        return self.fixed_dividend * self.par_value


class GlobalBeverageCorporationExchange:

    """The whole exchange where the trades take place"""

    def __init__(self,
                 stocks: [Stock]):
        """
        :param stocks: The stocks traded at this exchange.
        :raise ValueError:
        """
        if len(stocks) > 0:
            self.stocks = stocks
        else:
            msg = "Argument stocks={stocks} should be a non empty sequence.".format(stocks=stocks)
            raise ValueError(msg)

    def record_trade(self,
                     trade: Trade):
        """Records a trade for the proper stock.
        :param trade: The trade to record.
        """
        stock = next(stock for stock in self.stocks
                     if stock.ticker_symbol is trade.ticker_symbol)
        stock.record_trade(trade)

    def all_share_index(self,
                        current_time: datetime=datetime.now()) -> float:
        """
        :param current_time: The point of time for which we want to obtain the index.
        :return: The geometric mean of all stock prices. Returns None if any of them is
            None.
        """
        n = len(self.stocks)
        stock_prices = [stock.price(current_time) for stock in self.stocks]

        if None in stock_prices:
            return None
        else:
            product = reduce(operator.mul, stock_prices, 1)
            return product**(1/n)

