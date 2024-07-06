import asyncio
import schedule
import subprocess
import bot
import news_util

def scrape_economic_news(region):
    try:
        subprocess.run(["python", "news_scraper.py", region], check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error scraping economic news for {region}: {e}")

def scrape_upcoming_events():
    try:
        subprocess.run(["node", "event_scraper.js"], check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error scraping upcoming events: {e}")

def scrape_community_sentiment():
    try:
        subprocess.run(["python", "sentiment_scraper.py"], check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error scraping community sentiments: {e}")

# Main async function to run scheduled tasks
async def main():
    schedule.every().day.at("00:05").do(scrape_upcoming_events)
    schedule.every().day.at("00:10").do(scrape_community_sentiment)
    schedule.every().hour.at(":58").do(news_utiltil.clear_economic_news_files)

    schedule.every().hour.at(":00").do(scrape_economic_news, "US")
    schedule.every().hour.at(":20").do(scrape_economic_news, "EU")
    schedule.every().hour.at(":40").do(scrape_economic_news, "AS")

    while True:
        schedule.run_pending()
        await asyncio.sleep(60)
        await bot.send_upcoming_events()

if __name__ == "__main__":
    asyncio.run(main())