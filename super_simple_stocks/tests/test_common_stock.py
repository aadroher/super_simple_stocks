import unittest

from .factories import StockFactory, TradeFactory


class CommonStockDividendTestCase(unittest.TestCase):

    def setUp(self):
        self.stock = StockFactory.get_common_stock()

    def test_dividend_value(self):
        expected_value = self.stock.last_dividend
        self.assertEqual(self.stock.dividend, expected_value)


