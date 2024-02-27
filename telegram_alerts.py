# telegram_alerts.py
import requests
import json

def load_telegram_credentials():
    with open('credentials_telegram.json') as f:
        credentials = json.load(f)
    return credentials

def send_telegram_message(message):
    credentials = load_telegram_credentials()
    bot_token = credentials['Telegram_bot_token']
    chat_id = credentials['Telegram_chat_id']
    send_text = f'https://api.telegram.org/bot{bot_token}/sendMessage?chat_id={chat_id}&parse_mode=Markdown&text={message}&disable_web_page_preview=True'
    response = requests.get(send_text)
    return response.json()
