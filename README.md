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

- Detects multiple technical analysis patterns (e.g., MTR and more is coming)  
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

Get the list of equity from ListofSecurities or scraping online first before usage

Run the bot with:
```
main.py
```

The bot will connect to Discord and start monitoring configured stocks. Notifications will be pushed to the specified Discord channel when patterns are detected.

---

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

---

## Disclaimer

**This bot is for educational and research purposes only. It is NOT financial advice or a trading recommendation. Use at your own risk.**

