import requests
import json
import pandas as pd
from binance.client import Client
import datetime
import schedule
import time
from alert_levels_tg import get_volume_alert_details
from telegram_alerts import send_telegram_message  # Import the Telegram alert function
from formatting_btk import format_number, generate_chart_url

def generate_binance_chart_url(symbol, interval="1h"):
    base_url = "https://www.tradingview.com/chart/"
    chart_params = f"symbol=BINANCE:{symbol}&interval={interval}"
    return f"{base_url}?{chart_params}"

def run_script():
    # Load Binance credentials
    with open('credentials_b.json') as f:
        credentials = json.load(f)
    api_key = credentials['Binance_api_key']
    api_secret = credentials['Binance_secret_key']
    client = Client(api_key, api_secret)
    
    # Fetch symbols for analysis
    symbols = client.get_exchange_info()['symbols']
    usdt_pairs = [s['symbol'] for s in symbols if (s['quoteAsset'] == 'USDT' or s['quoteAsset'] == 'BUSD') and 'UPUSDT' not in s['symbol']
                  and 'DOWNUSDT' not in s['symbol'] and 'UPBUSD' not in s['symbol'] and 'DOWNBUSD' not in s['symbol'] and 'BEARUSDT' not
                  in s['symbol'] and 'BULLUSDT' not in s['symbol'] and 'BEARBUSD' not in s['symbol'] and 'BULLBUSD' not in s['symbol']
                  and 'BCHSVUSDT' not in s['symbol'] and 'BCHABUSD' not in s['symbol'] and 'DNTUSDT' not in s['symbol']
                  and 'BTCSTUSDT' not in s['symbol'] and 'USDSUSDT' not in s['symbol'] and 'USDPUSDT' not in s['symbol']
                  and 'STRATUSDT' not in s['symbol'] and 'SUSDUSDT' not in s['symbol'] and 'WNXMBUSD' not in s['symbol'] and
                  'WNXMUSDT' not in s['symbol']] 
    
    for symbol in usdt_pairs:
        interval = '1h'
        limit = 25
        url = f'https://api.binance.com/api/v3/klines?symbol={symbol}&interval={interval}&limit={limit}'
        try:
            response = requests.get(url)
            response.raise_for_status()
            data = response.json()
            df = pd.DataFrame(data, columns=["timestamp", "open", "high", "low", "close", "volume", "close_time", "quote_asset_volume", "number_of_trades", "taker_buy_base_asset_volume", "taker_buy_quote_asset_volume", "ignore"])
            df["timestamp"] = pd.to_datetime(df["timestamp"], unit="ms")
            df["volume"] = pd.to_numeric(df["volume"])
            
            if len(df) > 2:
                curr_volume = df['volume'].iloc[-2]
                past_24_hours = df.iloc[:-2]['volume'].astype(float)
                prev_volume_mean = past_24_hours.mean()
                
                alert_details_list = get_volume_alert_details(curr_volume, prev_volume_mean, symbol, '1h', 'BINANCE')

                
            for alert_detail in alert_details_list:
                alert_message = {
                    'exchange': 'BINANCE',
                    'symbol': alert_detail['symbol'],
                    'curr_volume': alert_detail['curr_volume'],
                    'prev_volume_mean': alert_detail['prev_volume_mean'],
                    'level': alert_detail['level'],
                    'chart_url': alert_detail['chart_url']
                }
                send_telegram_message(alert_message)

        except requests.exceptions.RequestException as e:
            print(f"Error fetching data for {symbol}: {e}")
        except ValueError as e:
            print(f"Error processing data for {symbol}: {e}")

run_script()
# Schedule the script to run at the specified times
#for hour in range(24):
    #schedule.every().day.at("{:02d}:01".format(hour)).do(run_script)

# Run the scheduled tasks indefinitely
#while True:
    #schedule.run_pending()
    #time.sleep(1)
