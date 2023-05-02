import yfinance as yf
import pandas as pd
import time

# Define the ticker symbol of the asset you are interested in
ticker = "L&TFH.NS"

# Define the span of the EMA
ema_span = 5

# Define a variable to keep track of the alert candle
alert_candle = None

# Function to find alert candles
def find_alert():
    global alert_candle
    
    # Continuously retrieve the most recent closing price and calculate the EMA
    while True:
        # Use yfinance to get the most recent price data for the past 5 minutes
        data = yf.download(ticker, period="1d", interval="5m")
        
        # Calculate the EMA with the given span using the most recent closing prices
        ema = data["Close"].ewm(span=ema_span, adjust=False).mean()
        
        # Get the latest 5-minute candle
        latest_candle = data.iloc[-1]
        print(latest_candle)
        
        # Check if the low of the latest candle is above the EMA
        if latest_candle["Low"] > ema.iloc[-1]:
            alert_candle = latest_candle
            print("Alert candle found at: ", latest_candle.name, latest_candle)
            return alert_candle
            
        # Wait for a certain amount of time before retrieving the next set of price data
        time.sleep(300)

# Function to check for trade opportunities
def check_trade():
    global alert_candle
    
    while True:
        # Check if there is an alert candle
        if alert_candle is None:
            # Call find_alert() to get the next alert candle
            find_alert()
            
        # Define a flag to check if alert candle breaks
        alert_break = False
        
        # Loop for 5 minutes to wait for the alert candle to break
        for i in range(5):
            # Define the start and end time of the 1-minute window
        

            # Use yfinance to get the most recent price data for the past 1 minute
            data = yf.download(ticker, period="1d", interval="1m")
            latest_candle = data.iloc[-1]

            # Check if the low of the latest candle breaks the low of the alert candle
            if latest_candle["Low"] < alert_candle["Low"]:
                print("Trade taken at: ", latest_candle.name)
                # Place your trade here
                alert_candle = None
                alert_break = True
                break
            
            # Wait for a minute before checking the next 1-minute candle
            time.sleep(60)
        
        # If alert candle didn't break in 5 minutes, call find_alert() again to get the next alert candle
        if not alert_break:
            alert_candle = None
            find_alert()

# Start the check_trade thread
check_trade()
