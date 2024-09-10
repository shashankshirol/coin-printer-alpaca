from alpaca.trading.client import TradingClient
from alpaca.trading.requests import MarketOrderRequest
from alpaca.trading.enums import OrderSide, OrderStatus, OrderType, TimeInForce

import time

import utils
import fetch_data

CONFIG = utils.load_config("config.toml")
API_KEY = CONFIG["api"]["key"]
SECRET = CONFIG["api"]["secret"]

GENERATE_BACKTEST_DATA = False


def get_order(default: bool = True) -> MarketOrderRequest:

    if default:
        params = dict(
            symbol="SPY",
            qty=0.5,
            side=OrderSide.BUY,
            time_in_force=TimeInForce.DAY
        )
    else: # use appropriate trading strategies to come up with the right trade
        params = dict()

    return MarketOrderRequest(**params)



def trader(client: TradingClient, debug: bool = True):
    while True and not debug:
        print("Running the Trader\nPress CTRL + C to quit.")
        order_data = get_order()
        print(client.submit_order(order_data))
        time.sleep(3)


if __name__ == "__main__":
    trading_client = TradingClient(API_KEY, SECRET, paper=True)
    trader(trading_client)

    GENERATE_BACKTEST_DATA and fetch_data.generate_data(False)

    pass