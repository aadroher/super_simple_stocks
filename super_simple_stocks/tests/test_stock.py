import unittest

from ..model import TickerSymbol, Stock
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
