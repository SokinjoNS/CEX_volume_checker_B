#import all requred libraries, install them using pip command first
import requests
import os
import time
import json
import pandas as pd
from binance.client import Client
import datetime
import schedule


now = datetime.datetime.now()
# Calculate the remaining time to the next full hour
remaining_minutes = 60 - now.minute - 1
remaining_seconds = 60 - now.second
remaining_time = remaining_minutes * 60 + remaining_seconds


# Load credentials from credentials.json
with open('credentials_b.json') as f:
    credentials = json.load(f)

# Retrieve API key and secret from credentials
api_key = credentials['Binance_api_key']
api_secret = credentials['Binance_secret_key']

# get your telegram bot token and chat id
with open('credentials_telegram.json') as f:
    credentials = json.load(f)

bot_token = credentials['Telegram_bot_token']
chat_id = credentials['Telegram_chat_id']

client = Client(api_key, api_secret)

def generate_binance_chart_url(symbol, interval="1h"):
    base_url = "https://www.tradingview.com/chart/"
    chart_params = f"symbol=BINANCE:{symbol}&interval={interval}"
    return f"{base_url}?{chart_params}"



def run_script():
    # List of symbols included in the script, excluding the stablecoins and other irrelevant pairs
    symbols = client.get_exchange_info()['symbols']
    usdt_pairs = [s['symbol'] for s in symbols if (s['quoteAsset'] == 'USDT' or s['quoteAsset'] == 'BUSD') and 'UPUSDT' not in s['symbol']
                  and 'DOWNUSDT' not in s['symbol'] and 'UPBUSD' not in s['symbol'] and 'DOWNBUSD' not in s['symbol'] and 'BEARUSDT' not
                  in s['symbol'] and 'BULLUSDT' not in s['symbol'] and 'BEARBUSD' not in s['symbol'] and 'BULLBUSD' not in s['symbol']
                  and 'BCHSVUSDT' not in s['symbol'] and 'BCHABUSD' not in s['symbol'] and 'DNTUSDT' not in s['symbol']
                  and 'BTCSTUSDT' not in s['symbol'] and 'USDSUSDT' not in s['symbol'] and 'USDPUSDT' not in s['symbol']
                  and 'STRATUSDT' not in s['symbol'] and 'SUSDUSDT' not in s['symbol'] and 'WNXMBUSD' not in s['symbol'] and
                  'WNXMUSDT' not in s['symbol']] 


    for symbol in usdt_pairs:
        interval = '1h' # Retrieve data for previous 25 hours with 1 hour interval
        limit = 25
        url = f'https://api.binance.com/api/v3/klines?symbol={symbol}&interval={interval}&limit={limit}'

        try:
            response = requests.get(url)
            response.raise_for_status()  # raise an exception if status code is not 200

            data = response.json()
            df = pd.DataFrame(data, columns=["timestamp", "open", "high", "low", "close", "volume",
                                             "close_time", "quote_asset_volume", "number_of_trades",
                                             "taker_buy_base_asset_volume", "taker_buy_quote_asset_volume",
                                             "ignore"])

            # convert timestamp to datetime
            df["timestamp"] = pd.to_datetime(df["timestamp"], unit="ms")

            # convert volume to numeric
            df["volume"] = pd.to_numeric(df["volume"])

            # calculate volume change
            if len(df) > 2:
                curr_volume = df['volume'].iloc[-2]
                past_24_hours = df.iloc[:-2]['volume'].astype(float)
                prev_volume_mean = past_24_hours.mean()
                
                # here you defined the percentages (%) of increase that you want to be notified on, and their different levels
                if curr_volume > prev_volume_mean * 15:
                    # send alert message for 1500% +
                    message = f"*Binance*\n"
                    message += f"*{symbol}* volume spike of over *1500%* in the last 1h!!!!!"
                    message += f"\n\nCurrent volume: *{curr_volume:.2f}*"
                    message += f"\nVolume MA in past 24h: *{prev_volume_mean:.2f}*"
                    message += "\n\n🚀🚀🚀🚀🚀🔴🚀🔴🚀🔴🚀🚀🚀🚀🚀"

                    chart_url = generate_binance_chart_url(symbol, interval)
                    message += f'\n\n[Open Binance Chart]({chart_url})'
                    requests.get(f'https://api.telegram.org/bot{bot_token}/sendMessage?chat_id={chat_id}&parse_mode=Markdown&text={message}&disable_web_page_preview=True')
                        
                elif curr_volume > prev_volume_mean * 10:
                    # send alert message for 1000% +
                    message = f"*Binance*\n"
                    message += f"*{symbol}* volume spike of over *1000%* in the last 1h!!!!!"
                    message += f"\n\nCurrent volume: *{curr_volume:.2f}*"
                    message += f"\nVolume MA in past 24h: *{prev_volume_mean:.2f}*"
                    message += "\n\n🚀🚀🚀🔴🔴🔴🚀🚀🚀"
                    
                    chart_url = generate_binance_chart_url(symbol, interval)
                    message += f'\n\n[Open Binance Chart]({chart_url})'
                    requests.get(f'https://api.telegram.org/bot{bot_token}/sendMessage?chat_id={chat_id}&parse_mode=Markdown&text={message}&disable_web_page_preview=True')
                            
                elif curr_volume > prev_volume_mean * 7:
                    # send alert message for 700%
                    message = f"*Binance*\n"
                    message += f"*{symbol}* volume spike of over *700%* in the last 1h!!!!!"
                    message += f"\n\nCurrent volume: *{curr_volume:.2f}*"
                    message += f"\nVolume MA in past 24h: *{prev_volume_mean:.2f}*"
                    message += "\n\n🔴🚨🔴"
                    
                    chart_url = generate_binance_chart_url(symbol, interval)
                    message += f'\n\n[Open Binance Chart]({chart_url})'
                    requests.get(f'https://api.telegram.org/bot{bot_token}/sendMessage?chat_id={chat_id}&parse_mode=Markdown&text={message}&disable_web_page_preview=True')

                elif curr_volume > prev_volume_mean * 5:
                    # send alert message for 500% +
                    message = f"*Binance*\n"
                    message += f"*{symbol}* volume spike of over *500%* in the last 1h!!!!!"
                    message += f"\n\nCurrent volume: *{curr_volume:.2f}*"
                    message += f"\nVolume MA in past 24h: *{prev_volume_mean:.2f}*"
                    message += "\n\n🚨🚨🚨"
                    
                    chart_url = generate_binance_chart_url(symbol, interval)
                    message += f'\n\n[Open Binance Chart]({chart_url})'
                    requests.get(f'https://api.telegram.org/bot{bot_token}/sendMessage?chat_id={chat_id}&parse_mode=Markdown&text={message}&disable_web_page_preview=True')                  

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





