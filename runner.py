from alpaca.trading.client import TradingClient
from alpaca.trading.requests import MarketOrderRequest
from alpaca.trading.enums import OrderSide, OrderStatus, OrderType, TimeInForce

import time
import toml

def load_config(filename: str):
    return toml.load(filename)

def create_trader_client(config: dict):
    return TradingClient(config["api"]["key"], config["api"]["secret"], paper=True)

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



def trader(client: TradingClient):
    while True:
        print("Running the Trader\nPress CTRL + C to quit.")
        order_data = get_order()
        print(client.submit_order(order_data))
        time.sleep(3)


if __name__ == "__main__":
    config = load_config("config.toml")
    trader(create_trader_client(config=config))
    pass