from super_simple_stocks import (TickerSymbol,
                                 CommonStock,
                                 PreferredStock,
                                 BuySellIndicator)

STOCKS = (
    (TickerSymbol.TEA, CommonStock, 0.0, None, 100.0),
    (TickerSymbol.POP, CommonStock, 8.0, None, 100.0),
    (TickerSymbol.ALE, CommonStock, 23.0, None, 60.0),
    (TickerSymbol.GIN, PreferredStock, 8.0, 0.02, 100.0),
    (TickerSymbol.JOE, CommonStock, 13.0, None, 250.0)
)

TRADES = (
    (TickerSymbol.TEA, '1929-10-24T09:30:01', 500, 80.0, BuySellIndicator.BUY),
    (TickerSymbol.TEA, '1929-10-24T09:35:00', 2560, 72.0, BuySellIndicator.BUY),
    (TickerSymbol.TEA, '1929-10-24T09:41:23', 750, 78.0, BuySellIndicator.BUY),
    (TickerSymbol.TEA, '1929-10-24T09:53:40', 1750, 77.5, BuySellIndicator.BUY),
    (TickerSymbol.TEA, '1929-10-24T10:22:38', 250, 81.0, BuySellIndicator.BUY),
    (TickerSymbol.GIN, '1929-10-24T09:45:13', 170, 102.0, BuySellIndicator.BUY),
    (TickerSymbol.GIN, '1929-10-24T10:10:10', 220, 101.0, BuySellIndicator.BUY),
    (TickerSymbol.GIN, '1929-10-24T10:12:30', 350, 98.0, BuySellIndicator.BUY),
    (TickerSymbol.GIN, '1929-10-24T10:13:05', 80, 100.0, BuySellIndicator.BUY),
)







