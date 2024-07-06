# Forex News Telebot

## Overview
Forex News Telegram bot is an automated system designed to provide comprehensive updates on forex-related news and events. The bot operates in three main parts: Sentiment Analysis, News Scraping, and Upcoming Events. It scrapes news articles, preprocesses the data, performs NLP tasks, and sends summarized news updates to a Telegram channel.

## Table of Contents
- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [Example Usage](#example-usage)
- [Technologies Used](#technologies-used)

## Features
- **Sentiment Analysis**: Uses Myfxbook API to retrieve community sentiment data once a day.
- **News Scraping**: Hourly scrapes relevant news from news site and delivers concise summaries using data preprocessing and NLP.
- **Upcoming Events**: Scrapes high and medium impact upcoming events from Forex Factory and sends updates daily.
- **Telegram Integration**: Uses a Telegram bot to deliver updates to a specified channel.

## Installation

1. **Clone the repository**
    ```sh
    git clone https://github.com/lkjearl/Forex-News-Telebot.git
    cd telegram-news-bot
    ```

2. **Set up a virtual environment**
    ```sh
    python -m venv venv
    source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
    ```

3. **Install the required Python packages**
    ```sh
    pip install -r requirements.txt
    ```

4. **Set up environment variables**
    Create a `.env` file in the root directory and add the following variables:
    ```sh
    TELEGRAM_TOKEN=<your_telegram_bot_token>
    TELEGRAM_CHANNEL_ID=<your_telegram_channel_id>
    MYFXBOOK_EMAIL=<your_myfxbook_email>
    MYFXBOOK_PASSWORD=<your_myfxbook_password>
    ```

## Usage

1. **Run the main script**
    ```sh
    python main.py
    ```
2. **Graceful stop script**
    Ctrl + C in terminal

## Example Usage
    -

## Technologies Used

- Python
- Node.js
- Spacy
- BeautifulSoup
- Telegram API
- Myfxbook API
- Puppeteer
- Asyncio
- Schedule
- Decouple