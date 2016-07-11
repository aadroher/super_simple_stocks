import unittest

from .factories import StockFactory, TradeFactory

from ..model import GlobalBeverageCorporationExchange, TickerSymbol


class GlobalBeverageCorporationExchangeInitTestCase(unittest.TestCase):

    def test_checks_empty_stocks(self):
        with self.assertRaises(ValueError):
            gbce = GlobalBeverageCorporationExchange([])


class GlobalBeverageCorporationExchangeRecordAllShareIndexTestCase(unittest.TestCase):

    def test_not_enough_significant_trades_returns_none(self):
        stocks = StockFactory.get_stocks()
        gbce = GlobalBeverageCorporationExchange(stocks)
        index = gbce.all_share_index()
        self.assertIsNone(index)

    def test_index_value(self):

        tea_stock = StockFactory.get_stock_by_ticker_symbol(TickerSymbol.TEA)
        gin_stock = StockFactory.get_stock_by_ticker_symbol(TickerSymbol.GIN)
        gbce = GlobalBeverageCorporationExchange([tea_stock, gin_stock])

        tea_stock_trades = TradeFactory.get_trades_for_stock(TickerSymbol.TEA)
        gin_stock_trades = TradeFactory.get_trades_for_stock(TickerSymbol.GIN)

        for trade in tea_stock_trades + gin_stock_trades:
            gbce.record_trade(trade)

        last_tea_stock_trade = sorted(tea_stock_trades,
                                      key=lambda t: t.timestamp,
                                      reverse=True)[0]
        last_gin_stock_trade = sorted(gin_stock_trades,
                                      key=lambda t: t.timestamp,
                                      reverse=True)[0]

        current_time = max([last_tea_stock_trade.timestamp,
                            last_gin_stock_trade.timestamp])
        tea_stock_price = tea_stock.price(current_time)
        gin_stock_price = gin_stock.price(current_time)
        expected_value = (tea_stock_price * gin_stock_price)**(1/2)

        self.assertEqual(gbce.all_share_index(current_time), expected_value)





