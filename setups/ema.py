# from datetime import datetime, time, timedelta
# import yfinance as yf
# import ta.trend as tr

# stock = "RELIANCE.NS"
# start_date = datetime.now().strftime("%Y-%m-%d")
# end_date = datetime.now().strftime("%Y-%m-%d")

# # Download stock data from Yahoo Finance
# df = yf.download(stock, start=start_date, end=end_date, interval='5m')

# # Set up parameters
# stop_loss = None
# trigger_price = None
# entry_price = None
# position_size = 1
# risk_reward_ratio = 2.5
# max_loss_pct = 0.02

# # Calculate EMA
# df['ema'] = tr.ema_indicator(df['Close'], window=5)

# # Loop through each row of the dataframe
# for i in range(1, len(df)):
    
#     # Check if it's a new trading day and reset stop loss and trigger price
#     if df.index[i].date() != df.index[i-1].date():
#         stop_loss = None
#         trigger_price = None
    
#     # Check if it's between 9:15 and 10:00 AM
#     if df.index[i].time() >= time(9, 15) and df.index[i].time() <= time(10, 0):
        
#         # Check if the current candle is below the EMA and if stop loss and trigger price are not set
#         if df['Close'][i] < df['ema'][i] and not stop_loss and not trigger_price:
            
#             # Set trigger price to low of next red candle
#             for j in range(i+1, len(df)):
#                 if df['Close'][j] < df['Close'][j-1] and df['Low'][j] < df['ema'][j]:
#                     trigger_price = df['Low'][j]
#                     break
                    
#             # If trigger price is set, set stop loss to high of green candle that triggered it
#             if trigger_price:
#                 for j in range(i, len(df)):
#                     if df['Close'][j] > df['Close'][j-1] and df['High'][j] > df['ema'][j]:
#                         stop_loss = df['High'][j]
#                         entry_price = df['Close'][i]
#                         break
                        
#         # Check if stop loss and trigger price are set
#         elif stop_loss and trigger_price:
            
#             # Check if the current candle is below the trigger price
#             if df['Low'][i] < trigger_price:
                
#                 # Calculate the risk and reward
#                 risk = entry_price - stop_loss
#                 reward = risk_reward_ratio * risk
                
#                 # Set the take profit and stop loss prices
#                 take_profit = entry_price - reward
#                 stop_loss = entry_price + risk
                
#                 # Calculate the position size based on max loss percentage
#                 max_loss = max_loss_pct * entry_price
#                 position_size = round(max_loss / risk)
                
#                 # Print the trade details
#                 print(f"Entry Price: {entry_price:.2f}")
#                 print(f"Take Profit: {take_profit:.2f}")
#                 print(f"Stop Loss: {stop_loss:.2f}")
#                 print(f"Position Size: {position_size}")
#                 print(f"Risk Reward Ratio: {risk_reward_ratio}")
#                 print("------------------------------")
                
#                 # Reset stop loss and trigger price
#                 stop_loss = None
#                 trigger_price = None

import yfinance as yf
import pandas as pd
import time
import threading

alert_candle = None
count =1
def calculate_ema(symbol, ema_period):
    # Load data for the symbol
    data = yf.download(symbol, period="1d", interval="5m")
    
    # Calculate EMA for the symbol
    prices = data["Close"].to_list()
    ema = []
    ema.append(prices[0])
    multiplier = 2 / (ema_period + 1)
    for i in range(1, len(prices)):
        ema_value = (prices[i] - ema[-1]) * multiplier + ema[-1]
        ema.append(ema_value)
    
    return ema

def should_take_trade(symbol):
    global alert_candle
    global count
    ema = calculate_ema(symbol, 5)
    current_candle = yf.download(symbol, period="1d", interval="5m")
    current_price = current_candle["Close"][-1]
    current_low = current_candle["Low"][-1]
    if alert_candle is None:
        if current_low > ema[-1]:
            alert_candle = current_candle
            return None
        else:
            return None
    else:
        if current_low > ema[-1] and current_low > alert_candle["low"]:
            alert_candle = current_candle
            count +=1 
            return None
        elif current_low < alert_candle["low"]:
            if count >=2:
                entry_price = current_price
                stop_loss = max(alert_candle["high"], alert_candle["high"])
                target = entry_price - 2 * (entry_price - stop_loss)
                alert_candle = None
                return {"symbol": symbol, "entry_price": entry_price, "stop_loss": stop_loss, "target": target}
        else:
            return None

symbols = ["AAPL", "GOOG", "TSLA", "MSFT", "AMZN"]

def analyze_symbol(symbol):
    while True:
        trade = should_take_trade(symbol)
        if trade:
            print("Trade Alert:", trade)
        time.sleep(300)

# Create a thread for each symbol
threads = []
for symbol in symbols:
    thread = threading.Thread(target=analyze_symbol, args=(symbol,))
    threads.append(thread)

# Start all threads
for thread in threads:
    thread.start()

# Wait for all threads to complete
for thread in threads:
    thread.join()