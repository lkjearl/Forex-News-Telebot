import requests
import os
from bs4 import BeautifulSoup

# Constants
MAX_ARTICLES_TO_SCRAPE = 10
SCRAPE_LOG_FILE = 'scraped_articles.txt'

# Function to scrape individual article pages
def scrape_article(article_url):
    try:
        response = requests.get(article_url)
        response.raise_for_status()  # Check if the request was successful
        article_html = response.text
        soup = BeautifulSoup(article_html, 'html.parser')

        headline = soup.select_one('div.storyContent h1').text
        # If/else statement due to website structure
        author_elem = soup.select_one('span.spnAuthor a')
        if author_elem:
            author = author_elem.text
        else:
            # If <a> tag not found, check directly in <span.spnAuthor>
            author = soup.select_one('span.spnAuthor').text.strip()
        date = soup.select_one('span.spnDate time').text
        story_content = soup.select_one('div.storyMain').text

        if headline and author and date and story_content:
            article_data = {
                "headline": headline,
                "author": author,
                "date": date,
                "story_content": story_content,
                "article_url": article_url
            }
            return article_data
        else:
            print("Missing required metadata in article:", article_url)
            return None
    except requests.exceptions.RequestException as e:
        print(f"Error scraping article: {e}")
        return None

def is_article_scraped(article_url, scraped_urls):
    return article_url in scraped_urls

def save_article_data(article_data, filename):
    with open(filename, 'a', encoding='utf-8') as file:
        file.write("Headline: " + article_data["headline"] + "\n")
        file.write("Author: " + article_data["author"] + "\n")
        file.write("Date: " + article_data["date"] + "\n")
        file.write("Article URL: " + article_data["article_url"] + "\n")  # Include the article URL
        file.write("Story Content:\n" + article_data["story_content"] + "\n\n")

def clear_economic_news_files():
    try:
        os.remove('economic_news_us.txt')
        os.remove('economic_news_eu.txt')
        os.remove('economic_news_as.txt')
        print("Economic news files cleared.")
    except FileNotFoundError:
        pass
