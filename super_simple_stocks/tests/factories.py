from ..model import (TickerSymbol,
                     Trade,
                     Stock,
                     CommonStock,
                     PreferredStock)


from .fixture_data import STOCKS


class StockFactory:

    @staticmethod
    def get_stocks() -> [Stock]:

        stocks = []
        for stock_data in STOCKS:

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
