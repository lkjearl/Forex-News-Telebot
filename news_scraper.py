import asyncio
import requests
from bs4 import BeautifulSoup
import news_util
import data_process
import sys

REGION_URLS = {
    'AS': "https://www.rttnews.com/list/asian-economic-news.aspx",
    'EU': "https://www.rttnews.com/list/european-economic-news.aspx",
    'US': "https://www.rttnews.com/list/us-economic-news.aspx"
}

REGION_SCRAPE_FILES = {
    'AS': 'economic_news_as.txt',
    'EU': 'economic_news_eu.txt',
    'US': 'economic_news_us.txt'
}

async def scrape_economic_news(region):
    try:
        url = REGION_URLS[region]
        scrape_file = REGION_SCRAPE_FILES[region]
        max_articles = news_util.MAX_ARTICLES_TO_SCRAPE

        response = requests.get(url)
        response.raise_for_status()  # Check if the request was successful
        news_html = response.text
        soup = BeautifulSoup(news_html, 'html.parser')

        # Extract article links from the page, starting from the bottom (latest articles)
        article_links = [a["href"] for a in soup.select('div.storycontent div.article h2 a')]

        # Load the list of already scraped article URLs (create the file if it doesn't exist)
        try:
            with open(news_util.SCRAPE_LOG_FILE, 'r', encoding='utf-8') as file:
                scraped_urls = file.read().splitlines()
        except FileNotFoundError:
            scraped_urls = []

        # Initialize a list to store scraped article URLs temporarily
        scraped_urls_temp = []

        # Iterate through article links and scrape if not already scraped
        for article_link in article_links:
            if len(scraped_urls_temp) >= max_articles:
                break # If reached max articles

            if article_link not in scraped_urls:
                article_data = news_util.scrape_article(article_link)

                # Save the article data to a file
                if article_data:
                    news_util.save_article_data(article_data, scrape_file)

                    # Add the article URL to the temporary list
                    scraped_urls_temp.append(article_link)

        # NLP processing on the scraped article URLs
        await data_process.process_articles(scraped_urls_temp, region)

        # Update list of scraped article URLs
        with open(news_util.SCRAPE_LOG_FILE, 'a', encoding='utf-8') as file:
            file.write('\n'.join(scraped_urls_temp) + '\n')

    except requests.exceptions.RequestException as e:
        print(f"Error scraping {region} economic news: {e}")

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: python NewsScraper.py <region>")
        sys.exit(1)

    region = sys.argv[1]
    asyncio.run(scrape_economic_news(region))
