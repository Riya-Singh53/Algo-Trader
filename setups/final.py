# import yfinance as yf
# import pandas as pd
# import time
# import threading

# alert_candle = {}
# count = {}
# symbols = []
# lock = threading.Lock()

# def calculate_ema(symbol, ema_period):
#     # Load data for the symbol
#     data = yf.download(symbol, period="1d", interval="5m")
    
#     # Calculate EMA for the symbol
#     prices = data["Close"].to_list()
#     ema = []
#     ema.append(prices[0])
#     multiplier = 2 / (ema_period + 1)
#     for i in range(1, len(prices)):
#         ema_value = (prices[i] - ema[-1]) * multiplier + ema[-1]
#         ema.append(ema_value)
    
#     return ema

# def should_take_trade(symbol):
#     global alert_candle
#     global count
#     ema = calculate_ema(symbol, 5)
#     current_candle = yf.download(symbol, period="1d", interval="5m")
#     current_price = current_candle["Close"][-1]
#     current_low = current_candle["Low"][-1]
#     with lock:
#         if alert_candle.get(symbol) is None:
#             if current_low > ema[-1]:
#                 alert_candle[symbol] = current_candle
#                 return None
#             else:
#                 return None
#         else:
#             if current_low > ema[-1] and current_low > alert_candle[symbol]["Low"][-1]:
#                 alert_candle[symbol] = current_candle
#                 count[symbol] += 1
#                 return None
#             elif current_low < alert_candle[symbol]["Low"][-1]:
#                 if count[symbol] >= 2:
#                     entry_price = current_price
#                     stop_loss = max(alert_candle[symbol]["High"][-1], alert_candle[symbol]["High"][-2])
#                     target = entry_price - 2 * (entry_price - stop_loss)
#                     alert_candle[symbol] = None
#                     count[symbol] = 0
#                     return {"symbol": symbol, "entry_price": entry_price, "stop_loss": stop_loss, "target": target}
#             else:
#                 return None

# def run_trades():
#     while True:
#         for symbol in symbols:
#             trade = should_take_trade(symbol)
#             if trade:
#                 print("Trade Alert:", trade)
#         time.sleep(300)

# # Start a new thread to run the trades
# trades_thread = threading.Thread(target=run_trades)
# trades_thread.start()
import pandas as pd
import yfinance as yf
import time

# Define the ticker symbol of the asset you are interested in
ticker = "AAPL"

# Define the span of the EMA
ema_span = 5

# Continuously retrieve the most recent closing price and calculate the EMA
while True:
    # Use yfinance to get the most recent price data for the past 5 minutes
    data = yf.download(ticker, period="1d", interval="5m")
    print(data.iloc[-1])
    # Calculate the EMA with the given span using the most recent closing prices
    ema = data["Close"].ewm(span=ema_span, adjust=False).mean()
    
    # Print the most recent EMA value
    print("lllll")
    print("Current EMA({}) value: {:.2f}".format(ema_span, ema.iloc[-1]))
    
    # Wait for a certain amount of time before retrieving the next set of price data
    time.sleep(300)  # wait for 5 minutes before retrieving the next set of price data
