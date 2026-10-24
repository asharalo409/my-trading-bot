import ccxt
import pandas as pd
import pandas_ta as ta
import time
import os
from dotenv import load_dotenv

# এনভায়রনমেন্ট ভেরিয়েবল লোড করা (API Key নিরাপত্তার জন্য)
load_dotenv()

# এক্সচেঞ্জ কানেকশন
exchange = ccxt.binance({
    'apiKey': os.getenv('API_KEY'),
    'secret': os.getenv('SECRET_KEY'),
    'enableRateLimit': True,
})

def fetch_data(symbol='BTC/USDT'):
    # গত ১০০ ঘণ্টার ডেটা আনা
    bars = exchange.fetch_ohlcv(symbol, timeframe='1h', limit=100)
    df = pd.DataFrame(bars, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
    return df

def analyze_market(df):
    # SMA ক্যালকুলেশন
    df['SMA_20'] = ta.sma(df['close'], length=20)
    df['SMA_50'] = ta.sma(df['close'], length=50)
    return df

def trade():
    symbol = 'BTC/USDT'
    df = fetch_data(symbol)
    df = analyze_market(df)
    
    last_close = df['close'].iloc[-1]
    sma_20 = df['SMA_20'].iloc[-1]
    sma_50 = df['SMA_50'].iloc[-1]
    
    print(f"Price: {last_close} | SMA20: {sma_20} | SMA50: {sma_50}")
    
    # বাই/সেল লজিক (গোল্ডেন ক্রস)
    if sma_20 > sma_50:
        print("Signal: BUY (SMA20 crossed above SMA50)")
        # exchange.create_market_buy_order(symbol, amount) # আসল ট্রেড করার জন্য এটি আনকমেন্ট করুন
    elif sma_20 < sma_50:
        print("Signal: SELL (SMA20 crossed below SMA50)")
        # exchange.create_market_sell_order(symbol, amount) # আসল ট্রেড করার জন্য এটি আনকমেন্ট করুন

# বট লুপ (প্রতি ১ ঘণ্টায় একবার চলবে)
if __name__ == "__main__":
    while True:
        try:
            trade()
        except Exception as e:
            print(f"Error: {e}")
        time.sleep(3600)
