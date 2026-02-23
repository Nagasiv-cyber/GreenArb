"""
GreenArb - Live Market Data Injector
Pulls real-time tick data for USD/INR, Nifty 50, and ADRs (INFY/HDFC).
Streams data locally to `market_feed.json` for the EAA Gate to consume.
"""

import yfinance as yf
import json
import time
import os
from datetime import datetime

MARKET_FEED_PIPE = r"C:\Users\K.Visagan\.gemini\antigravity\scratch\GreenArb\market_feed.json"

# Define tickers
# Note: For INR/USD forex spread conversion
# Nifty 50: ^NSEI
# INFY NSE: INFY.NS | INFY ADR (NYSE): INFY
# HDFC Bank NSE: HDFCBANK.NS | HDFC ADR (NYSE): HDB
TICKERS = {
    "USD_INR": "INR=X",
    "NIFTY_50": "^NSEI",
    "INFY_NSE": "INFY.NS",
    "INFY_ADR": "INFY",
    "HDFC_NSE": "HDFCBANK.NS",
    "HDFC_ADR": "HDB"
}

def fetch_live_prices():
    """Fetch the latest available prices for our target basket."""
    prices = {}
    try:
        # Batch download for efficiency
        data = yf.download(list(TICKERS.values()), period="1d", interval="1m", progress=False)
        
        # Extract the latest 'Close' price for each ticker
        if not data.empty and 'Close' in data:
            for key, symbol in TICKERS.items():
                # Get the last non-NaN value
                latest_valid = data['Close'][symbol].dropna()
                if not latest_valid.empty:
                    prices[key] = float(latest_valid.iloc[-1])
                else:
                    prices[key] = 0.0
    except Exception as e:
        print(f"Error fetching live prices: {e}")
        
    return prices

def run_injector_loop():
    print("Starting Live Market Data Injector...")
    print(f"Monitoring: {list(TICKERS.keys())}")
    
    while True:
        prices = fetch_live_prices()
        
        # Add timestamp
        feed_data = {
            "timestamp": datetime.now().isoformat(),
            "prices": prices
        }
        
        # Write atomically to JSON pipe
        tmp_file = MARKET_FEED_PIPE + ".tmp"
        try:
            with open(tmp_file, 'w') as f:
                json.dump(feed_data, f, indent=2)
            os.replace(tmp_file, MARKET_FEED_PIPE)
            print(f"[{datetime.now().strftime('%H:%M:%S')}] Market Feed Updated: USD/INR={prices.get('USD_INR', 0):.2f}, INFY_NSE={prices.get('INFY_NSE', 0):.2f}, INFY_ADR={prices.get('INFY_ADR', 0):.2f}")
        except Exception as e:
            print(f"Error writing to pipe: {e}")
            
        # Poll every 5 seconds (to respect API limits while maintaining "live" feel for prototype)
        time.sleep(5)

if __name__ == "__main__":
    # In a real HFT environment, this would be a direct UDP multicast from exchange colocations.
    # For this prototype, we use REST pooling.
    run_injector_loop()
