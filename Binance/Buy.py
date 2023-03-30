from binance.client import Client
from binance.enums import *
import environment

# Replace API_KEY and API_SECRET with your own values
client = environment.get_futures_client()

orders = client.get_account()
# Get the most recent trades for ETHUSDT
ethusdt_trades = client.get_my_trades(symbol='ETHUSDT')
# Loop through the trades and find the most recent buy trade
for trade in reversed(ethusdt_trades):
    if trade['isBuyer']:
        buy_price = float(trade['price'])
        break

print(f"The most recent buy price of ETHUSDT is: {buy_price:.2f} USDT")
exit()

# Place a market order to buy ETHUSTD at current market price
order = client.create_order(
    symbol='ETHUSDT',
    side=SIDE_BUY,
    type=ORDER_TYPE_MARKET,
    quantity=1)

print(order)
