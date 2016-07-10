import random
import datetime

from typing import Tuple
from ..model import (TickerSymbol,
                     CommonStock,
                     PreferredStock)

STOCKS = (
    (TickerSymbol.TEA, CommonStock, 0.0, None, 100.0),
    (TickerSymbol.POP, CommonStock, 8.0, None, 100.0),
    (TickerSymbol.ALE, CommonStock, 23.0, None, 60.0),
    (TickerSymbol.GIN, PreferredStock, 8.0, 0.02, 100.0),
    (TickerSymbol.JOE, CommonStock, 13.0, None, 250.0)
)

SEED = 1984
START_TIMESTAMP = datetime.datetime(year=1929,
                                    month=10,
                                    day=24,
                                    hour=9,
                                    minute=30)

def generate_trades_data(n: int) -> [Tuple]:

    random.seed(SEED)
    ticker_symbols = (stock_data[0] for stock_data in STOCKS)

    timestamp = START_TIMESTAMP
    trades_data = []
    for i in range(n):
        ticker_symbol = random.choice(ticker_symbol)
        next_tick_in_ms = random.randrange(10, 2000)
        timestamp = timestamp + datetime.timedelta(milliseconds=next_tick_in_ms)
        quantity = random.randrange(25, 5000)




