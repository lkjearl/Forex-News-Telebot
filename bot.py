import telegram
import json
import os
from decouple import config

# Load environment variables from .env
TOKEN = config('TELEGRAM_TOKEN')
CHANNEL_ID = config('TELEGRAM_CHANNEL_ID')

bot = telegram.Bot(token=TOKEN)

async def send_upcoming_events():
    try:
        with open('upcoming_events.txt', 'r') as file:
            events_data = json.load(file)

        if not events_data:
            message = "📅 *Upcoming Events:*\n\n📌 _No medium or high impact news today._"
        else:
            message = format_upcoming_events(events_data)

        await send_message_to_channel(message)
        os.remove('upcoming_events.txt')

    except Exception as e:
        print(f"Error sending upcoming events: {e}")

async def send_sentiment_data():
    try:
        with open('sentiment_data.json', 'r') as file:
            sentiment_data = json.load(file)

        message = format_sentiment_data(sentiment_data)
        await send_message_to_channel(message)
        os.remove('sentiment_data.json')

        print("Sentiment data sent to Telegram channel.")

    except Exception as e:
        print(f"Error sending sentiment data: {e}")

async def send_processed_data(article_title, article_link, summary, article_date, region):
    try:
        prefix = get_prefix(region)
        truncated_summary = truncate_summary(summary)

        message = format_processed_data(prefix, article_title, article_link, article_date, truncated_summary)
        await send_message_to_channel(message)

    except Exception as e:
        print(f"Error processing data to send: {e}")

def format_upcoming_events(events_data):
    message = "📅 *Upcoming Events:*\n\n"
    medium_high_impact_count = 0

    for event in events_data:
        if event['impact'] in ['High Impact Expected', 'Medium Impact Expected']:
            medium_high_impact_count += 1
            impact_emoji = '🔴' if event['impact'] == 'High Impact Expected' else '🟠'
            message += f"{impact_emoji} {event['impact']} - {event['time']} - {event['event']}\n"
            message += f"   Currency: {event['currency']}\n\n"

    if medium_high_impact_count == 0:
        message += "📌 _No Medium or High impact news today._"

    return message

def format_sentiment_data(sentiment_data):
    message = "📊 *Sentiment Analysis*\n\n"
    for symbol, data in sentiment_data.items():
        message += f"🔹 {symbol}: 🟥_{data['shorts']}%_ | _{data['longs']}%_🟩\n"
    return message

def format_processed_data(prefix, article_title, article_link, article_date, truncated_summary):
    message = f"*{prefix}:* [{article_title}]({article_link})\n_{article_date}_\n\n{truncated_summary}"
    return message

async def send_message_to_channel(message):
    try:
        await bot.send_message(chat_id=CHANNEL_ID, text=message, parse_mode='Markdown', disable_web_page_preview=True)
    except Exception as e:
        print(f"Error sending message to Telegram: {e}")

def get_prefix(region):
    if region == "AS":
        return "Asia news"
    elif region == "US":
        return "US news"
    elif region == "EU":
        return "Europe news"
    else:
        return "Unknown news"  # For rare instances

def truncate_summary(summary, max_words=15):
    summary_words = summary.split()[:max_words]
    truncated_summary = ' '.join(summary_words)
    if len(summary_words) < len(summary.split()):
        truncated_summary += " ..."
    return truncated_summary
