from binance.client import Client
import pandas as pd
import pandas_ta as ta
import time
import environment

client = environment.get_futures_client()

maxRows = 120
symbol = 'ETHUSDT'
quantity = 1
timeframe = Client.KLINE_INTERVAL_5MINUTE
periods = 5*90
trailing_stop_offset = 0.01
ema_fast_period = 8
ema_slow_period = 22

def get_last_buy_price(stock):
    trades = client.get_my_trades(symbol=stock)
    # Loop through the trades and find the most recent buy trade
    for trade in reversed(trades):
        if trade['isBuyer']:
            buy_price = float(trade['price'])
            return buy_price
def calc_metrics(cp, MAX_ROWS):
    if len(cp) > MAX_ROWS:
        cp = cp.iloc[-MAX_ROWS:]
    cp.notna()
    cp['ema_fast'] = ta.sma(cp['close'], length=ema_fast_period)
    cp['ema_slow'] = ta.sma(cp['close'], length=ema_slow_period)
    cp['ema_crossed_below'] = False
    cp['ema_trend_down'] = False
    cp.loc[cp['ema_fast'] < cp['ema_slow'], 'ema_trend_down'] = True
    cp['ema_trend_up'] = False
    cp.loc[cp['ema_fast'] > cp['ema_slow'], 'ema_trend_up'] = True
    cp['high30'] = cp['close'].rolling(30, min_periods=1).max()
    cp['high60'] = cp['close'].rolling(60, min_periods=1).max()
    cp['high90'] = cp['close'].rolling(90, min_periods=1).max()
    cp['low30'] = cp['close'].rolling(30, min_periods=1).min()
    cp['low60'] = cp['close'].rolling(60, min_periods=1).min()
    cp['low90'] = cp['close'].rolling(90, min_periods=1).min()
    cp['high_30_60'] = cp.iloc[len(cp)-30]['high30']
    cp['high_60_90'] = cp.iloc[len(cp) - 60]['high30']
    cp['range_low_to_high'] = cp['high90'] - cp['low90']

    return cp


# Get historical klines data for the last 90 hours
klines = client.get_historical_klines(symbol, timeframe, f"{periods} minute ago UTC")
# e = pd.DataFrame()
# print(e.ta.indicators())

# Extract close prices from klines data
close_prices_start = pd.DataFrame([float(kline[4]) for kline in klines])
close_prices_start.columns = ['close']
close_prices = close_prices_start

# Calculate EMAs for the last 22 bars (including the current bar)
close_prices = calc_metrics(close_prices, maxRows)



buy_price = get_last_buy_price(symbol)
close_prices_last_row = close_prices.iloc[-1]

highest_high_price = close_prices_last_row['high90']
if buy_price > highest_high_price:
    highest_high_price = buy_price
# Calculate stop price as 3% below highest high price
stop_price = round(highest_high_price * (1 - trailing_stop_offset), 2)

# WHEN YOU START THIS LOGICWORK OUT IT YOU NEED TO SELL YOUR POSITION STRAIGHT AWAY OR PLACE A LIMIT SELL ORDER
# Is the market in dire straights and we sell or load now


# Place limit sell order with stop price and EMA conditions
if close_prices_last_row['ema_fast'] < close_prices_last_row['ema_slow'] and close_prices_last_row['close'] < stop_price:
    order = client.order_limit_sell(symbol=symbol, quantity=quantity, price=stop_price, stopPrice=stop_price)

    # Update stop price periodically to simulate trailing stop
    while True:
        # current_price = float(client.get_symbol_ticker(symbol=symbol)['price'])
        current_price = pd.DataFrame(data={'close': [float(client.get_symbol_ticker(symbol=symbol)['price'])]})

        # Calculate EMAs for the last 22 bars (including the current bar)
        # close_prices.append(current_price)
        close_prices_start = close_prices_start.append(current_price, ignore_index=True)
        close_prices = calc_metrics(close_prices_start, maxRows)
        close_prices_last_row = close_prices.iloc[-1]

        if current_price > stop_price:
            new_stop_price = round(current_price * (1 - trailing_stop_offset), 2)
            client.cancel_order(symbol=symbol, orderId=order['orderId'])
            if close_prices_last_row['ema_fast'] < close_prices_last_row['ema_slow']:
                order = client.order_limit_sell(
                    symbol=symbol,
                    quantity=quantity,
                    price=current_price,
                    stopPrice=new_stop_price,
                )
                stop_price = new_stop_price
            else:
                break
        elif current_price < stop_price:
            break
        time.sleep(5*60)
