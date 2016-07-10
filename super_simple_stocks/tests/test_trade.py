import unittest
from datetime import datetime

from ..model import Trade, BuySellIndicator


class TradeInitTestCase(unittest.TestCase):

    def test_init_args(self):
        pass


class TradeTotalPriceTestCase(unittest.TestCase):

    value_pairs = (
        (5000, 0.0),
        (5000, 27.25)
    )

    buy_sell_indicator = BuySellIndicator.BUY

    def test_total_price_value(self):

        for pair in self.value_pairs:
            expected_val = pair[0] / pair[1]
            trade = Trade(datetime.now(),
                          pair[0],
                          pair[1],
                          self.buy_sell_indicator)
            self.assertEqual(expected_val, trade.total_price)

