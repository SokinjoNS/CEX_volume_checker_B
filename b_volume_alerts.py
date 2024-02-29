# binance_volume_alerts.py
import requests
import json
import pandas as pd
from binance.client import Client
import datetime
import schedule
import time
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
                
                # here you define the percentages (%) of increase that you want to be notified on, and their different levels
                if curr_volume > prev_volume_mean * 15:
                    # send alert message for 1500% +
                    message = f"*Binance*\n"
                    message += f"*{symbol}* volume spike of over *1500%* in the last 1h!!!!!"
                    message += f"\n\nCurrent volume: *{format_number(curr_volume)}*"
                    message += f"\nVolume MA in past 24h: *{prev_volume_mean:.2f}*"
                    message += "\n\n🚀🚀🚀🚀🚀🔴🚀🔴🚀🔴🚀🚀🚀🚀🚀"
                    message += f"\n\n[Open Binance Chart]({generate_chart_url(symbol, 'BINANCE', interval)})"
                    send_telegram_message(message)  # Send the message using the Telegram script
                        
                elif curr_volume > prev_volume_mean * 10:
                    # send alert message for 1000% +
                    message = f"*Binance*\n"
                    message += f"*{symbol}* volume spike of over *1000%* in the last 1h!!!!!"
                    message += f"\n\nCurrent volume: *{format_number(curr_volume)}*"
                    message += f"\nVolume MA in past 24h: *{prev_volume_mean:.2f}*"
                    message += "\n\n🚀🚀🚀🔴🔴🔴🚀🚀🚀"
                    message += f"\n\n[Open Binance Chart]({generate_chart_url(symbol, 'BINANCE', interval)})"
                    send_telegram_message(message)  # Send the message using the Telegram script
                                             
                elif curr_volume > prev_volume_mean * 7:
                    # send alert message for 700%
                    message = f"*Binance*\n"
                    message += f"*{symbol}* volume spike of over *700%* in the last 1h!!!!!"
                    message += f"\n\nCurrent volume: *{format_number(curr_volume)}*"
                    message += f"\nVolume MA in past 24h: *{prev_volume_mean:.2f}*"
                    message += "\n\n🔴🚨🔴"
                    message += f"\n\n[Open Binance Chart]({generate_chart_url(symbol, 'BINANCE', interval)})"
                    send_telegram_message(message)  # Send the message using the Telegram script
                    
                elif curr_volume > prev_volume_mean * 5:
                    # send alert message for 500% +
                    message = f"*Binance*\n"
                    message += f"*{symbol}* volume spike of over *500%* in the last 1h!!!!!"
                    message += f"\n\nCurrent volume: *{format_number(curr_volume)}*"
                    message += f"\nVolume MA in past 24h: *{prev_volume_mean:.2f}*"
                    message += "\n\n🚨🚨🚨"
                    message += f"\n\n[Open Binance Chart]({generate_chart_url(symbol, 'BINANCE', interval)})"
                    send_telegram_message(message)  # Send the message using the Telegram script
                    
                
        except requests.exceptions.RequestException as e:
            print(f"Error fetching data for {symbol}: {e}")
        except ValueError as e:
            print(f"Error processing data for {symbol}: {e}")
# Schedule the script to run at the specified times
for hour in range(24):
    schedule.every().day.at("{:02d}:01".format(hour)).do(run_script)

# Run the scheduled tasks indefinitely
while True:
    schedule.run_pending()
    time.sleep(1) 
