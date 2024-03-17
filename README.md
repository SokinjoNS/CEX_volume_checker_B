# Binance Volume Monitor

__Description:__

The Binance Volume Checker is a Python script designed to monitor trading pairs on the Binance cryptocurrency exchange. It retrieves historical candlestick data for each trading pair, calculates the mean volume over the past 24 hours, and sends Telegram alerts if the current volume exceeds certain thresholds relative to the mean volume. This tool can help users identify significant volume spikes in cryptocurrency trading pairs.

## Features:

- Retrieves historical candlestick data for each trading pair from Binance.
- Calculates the mean volume over the past 24 hours.
- Sends Telegram alerts if the current volume exceeds certain thresholds.
- Customizable alert levels for different volume spike percentages.
- Includes links to TradingView charts for each trading pair.

## Installation:

__1. Clone the repository:__

```bash
git clone https://github.com/your_username/your_project.git
```

__2. Navigate to the project directory:__

```bash
cd your_project
```

__3. Install the required dependencies:__

```bash
pip install -r requirements.txt
```

__4. Obtain API credentials:__

You will need API credentials from Binance for accessing the Binance API.
Additionally, you will need a Telegram bot token and chat ID for sending alerts via Telegram.

__5. Create a__ _credentials_b.json_ file in the project directory and add your Binance API key and secret:

```bash
{
    "Binance_api_key": "YOUR_BINANCE_API_KEY",
    "Binance_secret_key": "YOUR_BINANCE_SECRET_KEY"
}
```

__6. Update__ the _bot_token_ and _chat_id_ variables in the script with your Telegram bot token and chat ID.

__Usage:__

Run the script:

```bash
python binance_volume_monitor.py
```

The script will start monitoring trading pairs on Binance. It will retrieve historical volume data, calculate the mean volume over the past 24 hours, and send Telegram alerts if the current volume exceeds certain thresholds.

The alerts will include information about the trading pair, current volume, mean volume over the past 24 hours, and a link to the TradingView chart for the trading pair.

## Contributing

Contributions are welcome! If you have ideas for new features, improvements, or bug fixes, feel free to fork the repository, make your changes, and submit a pull request. For major changes, please open an issue first to discuss what you would like to change.

## Support

For issues, questions, or contributions, please open an issue in the GitHub repository.

Feedback and contributions are welcome!

## License

This project is licensed under the MIT License - see the LICENSE file for details.
This project and the direct_address_tg_listener.py module are licensed under the MIT License. For more details, see the LICENSE file.
