import pandas as pd
import numpy as np
import talib as ta
import yfinance as yf
import time

ticker = 'AAPL'
timeframe = '5m'

interval = 300

alert_candle = None
previous_candle = None

def get_data():
    data = yf.download(ticker, period='1d', interval=timeframe)
    data['ema5'] = ta.EMA(data['Close'], timeperiod=5)
    return data

def execute_trade(action):
    print('Executing', action, 'trade')

def check_shorting_opportunities(data):
    global alert_candle, previous_candle
    latest_data = data.iloc[-1]
    if alert_candle is None:
        if latest_data['Low'] > latest_data['ema5']:
            alert_candle = latest_data
    else:
        if latest_data['Low'] > alert_candle['Low'] and latest_data['Close'] > alert_candle['ema5']:
            alert_candle = latest_data
        elif latest_data['Low'] < alert_candle['Low']:
            execute_trade('short')
            alert_candle = None
        elif previous_candle is not None and latest_data['Low'] < previous_candle['Low']:
            execute_trade('short')
            alert_candle = None
    previous_candle = latest_data

while True:
    data = get_data()
    check_shorting_opportunities(data)
    time.sleep(interval)