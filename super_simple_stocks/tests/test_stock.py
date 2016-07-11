import unittest
from datetime import timedelta, datetime

from ..super_simple_stocks import TickerSymbol, Stock
from .factories import StockFactory, TradeFactory


class StockInitTestCase(unittest.TestCase):

    def test_not_instantiable(self):

        with self.assertRaises(TypeError):
            stock = Stock(ticker_symbol=TickerSymbol.ALE,
                          par_value=100.0)


class StockRecordTradeTestCase(unittest.TestCase):

    def setUp(self):
        self.stock = StockFactory.get_stock()

    def test_checks_type(self):

        wrong_value = ('wrong', 'value')

        with self.assertRaises(TypeError):
            self.stock.record_trade(wrong_value)

    def test_trade_is_recorded(self):

        trade = TradeFactory.get_trade()
        self.stock.record_trade(trade)

        self.assertIn(trade, self.stock.trades)

    def test_checks_ticker_symbol(self):
        ale_stock = StockFactory.get_stock_by_ticker_symbol(TickerSymbol.ALE)
        tea_trade = TradeFactory.get_trade_for_stock(TickerSymbol.TEA)
        with self.assertRaises(ValueError):
            ale_stock.record_trade(tea_trade)


class StockTickerPriceTestCase(unittest.TestCase):

    def setUp(self):
        self.stock = StockFactory.get_stock()

    def test_empty_trades_raises_attribute_error(self):
        with self.assertRaises(AttributeError):
            ticker_price = self.stock.ticker_price

    def test_price_value(self):
        trade = TradeFactory.get_trade()
        self.stock.record_trade(trade)
        self.assertEqual(trade.price_per_share, self.stock.ticker_price)

    def test_price_value_is_last_trades(self):
        trades = TradeFactory.get_trades(3)
        last_trade = trades[-1]
        for trade in trades:
            self.stock.record_trade(trade)
        self.assertEqual(last_trade.price_per_share, self.stock.ticker_price)


class StockPriceEarningsRatioTestCase(unittest.TestCase):

    def test_zero_dividend_stock_returns_none(self):
        zero_dividend_stock = StockFactory.get_zero_dividend_stock()
        trade = TradeFactory.get_trade()
        zero_dividend_stock.record_trade(trade)
        pe_ratio = zero_dividend_stock.price_earnings_ratio
        self.assertIsNone(pe_ratio)


class StockPriceTestCase(unittest.TestCase):

    def setUp(self):
        self.stock = StockFactory.get_stock()

    def test_not_enough_significant_trades_returns_none(self):
        trade = TradeFactory.get_trade()
        self.stock.record_trade(trade)

        stock_price = self.stock.price()
        self.assertIsNone(stock_price)

    def test_price_value_for_one_trade(self):
        trade = TradeFactory.get_trade()
        self.stock.record_trade(trade)
        current_time = trade.timestamp + timedelta(minutes=10)

        expected_value = trade.price_per_share
        self.assertEqual(self.stock.price(current_time), expected_value)

    def test_price_value_for_multiple_trades(self):
        trades = TradeFactory.get_trades_for_stock(TickerSymbol.TEA)
        for trade in trades:
            self.stock.record_trade(trade)

        # Set the most recent trade timestamp as current_time.
        by_timestamp = sorted(trades,
                              key=lambda t: t.timestamp,
                              reverse=True)

        last_trade = by_timestamp[0]
        significant_trades = [trade for trade in trades
                              if trade.timestamp >=
                              last_trade.timestamp - self.stock.price_time_interval]
        trade_prices = (trade.total_price for trade in significant_trades)
        quantities = (trade.quantity for trade in significant_trades)
        expected_value = sum(trade_prices) / sum(quantities)

        self.assertEqual(self.stock.price(last_trade.timestamp), expected_value)


class CommonStockDividendTestCase(unittest.TestCase):

    def setUp(self):
        self.stock = StockFactory.get_common_stock()

    def test_dividend_value(self):
        expected_value = self.stock.last_dividend
        self.assertEqual(self.stock.dividend, expected_value)


class PreferredStockDividendTestCase(unittest.TestCase):

    def setUp(self):
        self.stock = StockFactory.get_preferred_stock()

    def test_dividend_value(self):
        expected_value = self.stock.fixed_dividend * self.stock.par_value
        self.assertEqual(self.stock.dividend, expected_value)
