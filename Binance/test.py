import binance_interaction as bi
import strategy
import environment

client = environment.get_spot_client()
# client = Spot(base_url=base_url, key=api_key, secret=secret_key)
print(client.time())
# print(client.klines("BTCUSDT","1m"))

# Get account and balance information
print("Client details")
response = client.account()
for x in response["balances"]:
    print(x)

# params = {
#     "symbol": "BTCUSDT",
#     "side": "BUY",
#     "type": "MARKET",
#     "quantity": 0.001,
# }
params = {'symbol': 'ETHBUSD', 'side': 'BUY', 'type': 'STOP_LOSS_LIMIT', 'timeInForce': 'GTC', 'quantity': 0.25, 'price': 1605.99, 'trailingDelta': 100}
# bi.make_trade_with_params(client=client, params=params)
# response = client.new_order(**params)
# print(response)
# print(client.my_trades(symbol="ETHUSDT"))
orders = bi.query_open_trades(client)
for order in orders:
    print(order)

# bi.cancel_all_orders_by_symbol(symbol="ETHBUSD", client=client)
# bi.cancel_order_by_id(symbol="ETHBUSD", id=9692171, client=client)


