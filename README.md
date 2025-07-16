# Technical-Analysis-Bot

A Discord bot that pushes notifications when specific stock patterns are detected. This bot is designed **solely for educational and research purposes** and **does NOT provide trading advice or suggestions**.

---

## Table of Contents

- [Introduction](#introduction)  
- [Features](#features)  
- [Installation](#installation)  
- [Usage](#usage)
- [License](#license)  
- [Disclaimer](#disclaimer)  

---

## Introduction
Technical-Analysis-Bot monitors stock price data and detects predefined technical patterns. When a pattern is identified, the bot sends real-time notifications to a Discord channel.

---

## Features

- Detects multiple technical analysis patterns (e.g., MTR and Golden Cross and more is coming)  
- Sends instant alerts to Discord channels  
- Supports multiple stock tickers simultaneously
- Designed for educational and research use

---

## Installation

1. Clone the repository:
```
git clone https://github.com/HugoYau/Technical-Analysis-Bot.git
cd Technical-Analysis-Bot
```

2. Install requirements:
```
pip install -r requirements.txt
```

3. Create your discord webhook bot (from Server Setting\Integrations\Create Webhook)

4. Copy the webhook url and paste it in myfun.py
```
#discord webhook url
bot_url = 'your-discord-bot-webhook-url'
```

---

## Usage

Get the list of equity from ListOfSecurities (you can get latest version from HKEX) or scraping online first before usage:
```
scraping.py
```

Run the bot with:
```
main.py
```

Change the time zone (if you want to) in myfun.py:
```
data.index = data.index.tz_convert('Asia/Hong_Kong')
```

**Initializing**

Enter whatever Ticker available in yahoo finance that you want to monitored. (NVDA, AAPL, ...)
```
"What stock do you want to monitor? (Enter Tickers with , to separate.)"
```
**Enter US for S&P500 components, HSI for HSI components (not up-to-date) and HK for all equity, ETFs, REITs in HKEX**
**Entering these will lead to a huge amount of notification. DONT try them unless you want.**

Enter what method you would like to use. (only MTR and Cross available now)
```
"What do you want to use to monitor the stock? (MTR or Cross or Both)"
```

Done. The bot will connect to Discord and start monitoring stocks. Notifications will be pushed to the specified Discord channel when patterns are detected.

**Using MTR will return the time when the price is at the recent highest point (Check the pattern after the time). Using Cross will return the time when the cross occur.**

---

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

---

## Disclaimer

**This bot is for educational and research purposes only. It is NOT financial advice or a trading recommendation. Use at your own risk.**

