import pandas as pd
import yfinance as yf

# Load historical data for the stock using the yfinance library
data = yf.download('BTC-USD', interval='5m', period='1d')

# Calculate the 5-period exponential moving average (EMA)
data["EMA5"] = data["Close"].ewm(span=5).mean()
print(data["EMA5"][-1])
# Initialize variables for tracking the current Alert Candle and the previous Alert Candle
current_alert_candle = None
previous_alert_candle = None

# Loop through each row in the data and execute the trading strategy
for i, row in data.iterrows():
    # If there is no current Alert Candle, check if the current candle is above the 5 EMA
    if current_alert_candle is None:
        if row["Close"] > row["EMA5"]:
            current_alert_candle = row
    # If there is a current Alert Candle, check if the next candle is above the 5 EMA without breaking the low of the previous Alert Candle
    else:
        if row["Close"] > row["EMA5"] and row["Low"] > previous_alert_candle["Low"]:
            current_alert_candle = row
        # If the next candle breaks the low of the current Alert Candle, take a short trade and set the stop loss and target
        elif row["Low"] < current_alert_candle["Low"]:
            stop_loss = current_alert_candle["High"]
            target = current_alert_candle["Close"] - 3 * (current_alert_candle["Close"] - current_alert_candle["Low"])
            print("Short trade: Entry price = ", row["Close"], " Stop loss = ", stop_loss, " Target = ", target)
            current_alert_candle = None
    # Set the previous Alert Candle to the current Alert Candle
    previous_alert_candle = current_alert_candle
