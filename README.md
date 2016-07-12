# Super Simple Stocks

This code is submitted as an answer to the assignment _Super Simple Stocks_ included in 
the hiring process for the position _Application Developer - 160060895_ at J.P.Morgan.
Its instructions may be found in the document `doc/SuperSimpleDocs.docx`.

## Requirements

Despite it being relatively rare in production environments, the application has been developed using Python 3 (3.5.2). This version has been chosen because Python 2._x_ is meant to end up being legacy code, this was a new project from scratch, and no third-party libraries where needed.     

## Code structure and usage

All the application proper is fully contained in the single top-level module `super_simple_stocks`. It is to be used by packing a set of instances of `Stock` in a sequence and pass it as the only argument to `GlobalBeverageCorporationExchange` initializer. The resulting instance is to be used a a representation of the complete GBCE. 

`Stock` itself is abstract, objects may only be created by means of its two inheriting classes, `CommonStock` and `PreferredStock`.

From that point on the method `GlobalBeverageCorporationExchange.record_trade` may be used to record new trades.

The calculations requested in the assignment instructions are then supplied by the following properties or methods:

- For a given instance of `Stock`:
  - _Calculate the dividend yield_: `Stock.dividend_yield`
  - _Calculate the P/E Ratio_: `Stock.price_earnings_ratio`
  - _Record a trade, with timestamp, quantity of shares, buy or sell indicator and price_: Create an instance of `Trade` and supply it to an instance of`GlobalBeverageCorporationExchange` that contains the proper stock my means of `record_trade`
  - _Calculate Stock Price based on trades recorded in past 15 minutes_: `Stock.price`
- _Calculate the GBCE All Share Index using the geometric mean of prices for all stocks_: `GlobalBeverageCorporationExchange.all_share_index`.

Type hints are present in all relevant signatures and basic documentation is included in the code itself.

## Tests

A moderately extensive (although my no means exhaustive) suite of tests is included in `tests/`. The autodiscovery feature of `unittest` makes it fairly convenient to run them by executing the following command:
 ````
$ git clone https://github.com/aadroher/super_simple_stocks
$ cd super_simple_stocks/
$ python -m unittest -v
````
The `-v` switch is optional and it stands for its verbose mode.






