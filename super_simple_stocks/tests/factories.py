from datetime import datetime

from ..model import (TickerSymbol,
                     Trade,
                     Stock,
                     CommonStock,
                     PreferredStock)


from .fixture_data import STOCKS, TRADES


class TradeFactory:

    @staticmethod
    def get_trades(n: int=len(TRADES)-1) -> [Trade]:

        trades = []
        for trade_data in TRADES[0:n+1]:
            trade = TradeFactory.from_tuple(trade_data)
            trades.append(trade)

        return trades

    @staticmethod
    def get_trade() -> Trade:
        return next(iter(TradeFactory.get_trades(1)))

    @staticmethod
    def get_trades_for_stock(ticker_symbol: TickerSymbol,
                             n: int=len(TRADES)-1):
        return [trade for trade in TradeFactory.get_trades()
                if trade.ticker_symbol is ticker_symbol][:n+1]

    @staticmethod
    def get_trade_for_stock(ticker_symbol: TickerSymbol):
        return next(iter(TradeFactory.get_trades_for_stock(ticker_symbol)))

    @staticmethod
    def from_tuple(trade_data: tuple) -> Trade:
        datetime_str_format = '%Y-%m-%dT%H:%M:%S'
        return Trade(ticker_symbol=trade_data[0],
                     timestamp=datetime.strptime(trade_data[1],
                                                 datetime_str_format),
                     quantity=trade_data[2],
                     price_per_share=trade_data[3],
                     buy_sell_indicator=trade_data[4])


class StockFactory:

    @staticmethod
    def get_stocks(n: int=len(STOCKS)-1) -> [Stock]:

        stocks = []
        for stock_data in STOCKS[0:n+1]:

            ticker_symbol = TickerSymbol(stock_data[0])
            par_value = stock_data[4]
            cls = stock_data[1]

            if cls is CommonStock:
                dividend = stock_data[2]
            elif cls is PreferredStock:
                dividend = stock_data[3]
            else:
                raise ValueError()

            stock = cls(ticker_symbol,
                        par_value,
                        dividend)
            stocks.append(stock)

        return stocks

    @staticmethod
    def get_stock() -> Stock:
        return next(iter(StockFactory.get_stocks(1)))

    @staticmethod
    def get_stock_by_ticker_symbol(ticker_symbol: TickerSymbol):
        return next(stock for stock in StockFactory.get_stocks()
                    if stock.ticker_symbol is ticker_symbol)

    @staticmethod
    def get_zero_dividend_stock() -> Stock:
        return next(stock for stock in StockFactory.get_stocks()
                    if stock.dividend == 0)

    @staticmethod
    def get_common_stock() -> CommonStock:
        return next(stock for stock in StockFactory.get_stocks()
                    if isinstance(stock, CommonStock))

    @staticmethod
    def get_preferred_stock() -> PreferredStock:
        return next(stock for stock in StockFactory.get_stocks()
                    if isinstance(stock, PreferredStock))




