## Algorithmic Stock Trader Enviroment


Uses the tdameritrade api to scan selected ticker. The ticker's attributes are then passed to an Equity class that 
contains:
- Fundamental Data or None
- Dataframe with a ytd price (open, close, high, low,) Along with moving averages and Historical Vol.
- Volatility Metrics or None
- A function which plots the basic graph in pyplot.

## Config File
> You must create a config.py file in the root directory containing the following variables and their values.



| Config File                     | default                                                                                | Description                                                                                                            |
| -------------------------------- | -------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------- |
| ALPACA_URL=        |                                                                                        | Your Alpaca Url        
| ALPACA_KEY=        |                                                                                        | Your Alpaca API Key                                                                                                           |
| ALPACA_SECRET= |                                                                                        | Your Alpaca API Secret Key       
| ameritrade= |                                                                                        | Your Td Ameritrade API Secret Key                                                              

> ## Run
```pip3 install -r requirements.txt```

> ### To run the algo as is 
> **WARNING**: Intended for PAPER TRADING ONLY

```python3 run.py```