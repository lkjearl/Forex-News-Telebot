import asyncio
import spacy
from spacy.lang.en.stop_words import STOP_WORDS
from heapq import nlargest
import news_util
import bot

# Load English tokenizer, tagger, parser, NER, and word vectors model
nlp = spacy.load("en_core_web_sm")

def clean_article(article_text):
    article_text = article_text.split("For comments and feedback contact")[0]
    return article_text

async def summarize_article(article_text, max_length=20):
    try:
        # Process using spacy model
        doc = nlp(article_text)
        
        sentence_scores = {}
        for sent in doc.sents:
            sentence_score = sum(word.is_alpha and not word.is_stop for word in sent)
            sentence_scores[sent] = sentence_score
        
        summary_sentences = nlargest(max_length, sentence_scores, key=sentence_scores.get)
        summary = ' '.join(sent.text for sent in summary_sentences).split()[:max_length]
        
        return ' '.join(summary)
    except Exception as e:
        print(f"Error summarizing article: {e}")
        return ''

async def process_articles(scraped_urls_temp, region):
    try:
        for article_url in scraped_urls_temp:
            article_data = news_util.scrape_article(article_url)
            if article_data:
                article_text = article_data.get("story_content", "")
                article_text = clean_article(article_text)
                summary = await summarize_article(article_text)
                
                article_title = article_data.get("headline", "")
                article_link = article_data.get("article_url", "")
                article_date = article_data.get("date", "")
                await bot.send_processed_data(article_title, article_link, summary, article_date, region)
    except Exception as e:
        print(f"Error processing articles: {e}")

    # Clear the economic news file contents after processing
    try:
        with open(news_util.SCRAPE_LOG_FILE, 'w', encoding='utf-8') as file:
            file.write('')
    except Exception as e:
        print(f"Error clearing the economic news file: {e}")
