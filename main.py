import asyncio
from datetime import datetime
import json
import importlib
from concurrent.futures import ThreadPoolExecutor, as_completed
import time
from database import get_recent_news_by_corporation, insert_news, insert_news_category
import os
from dotenv import load_dotenv

load_dotenv()

conn_params_production = {
    "host": os.getenv("DATABASE_HOST_PRODUCTION", "localhost"),
    "port": int(os.getenv("DATABASE_PORT_PRODUCTION", "3306")),  # Convert port to integer
    "user": os.getenv("DATABASE_USERNAME_PRODUCTION", "root"),
    "password": os.getenv("DATABASE_PASSWORD_PRODUCTION", "password"),
    "db": os.getenv("DATABASE_NAME_PRODUCTION", "newsdb"),
} 

def load_scraper(config):
    module_name = f"scraper.{config['module']}"
    class_name = config["class"]
    module = importlib.import_module(module_name)
    scraper_class = getattr(module, class_name)
    return scraper_class(config["base_url"], config["urls_blacklist"])


def datetime_converter(o):
    if isinstance(o, datetime):
        return o.__str__()

counter = 0

def fetch_and_scrape(scraper, url, recent_news):
    global counter
    if url in recent_news:
        counter += 1
        return None
    
    article_data = scraper.scrape_article(url)
    return article_data

async def insert_article_and_category(conn_params, article, corporation_id, corporation_name, corporation_logo, category_id):
    news = await insert_news(
        conn_params,
        title=article['title'],
        content=article['content'],
        publishedDate=article['date'],
        externalNewsURL=article['url'],
        imageURL=article['image_url'],
        corporationID=corporation_id,
        corporationName=corporation_name,
        corporationLogo=corporation_logo
    )
    if category_id != -1 and news.get("id"):
        await insert_news_category(conn_params, news.get("id"), category_id)

async def parallel_main():
    start_time = time.time()  # Start timing for overall execution

    with open('config.json') as file:
        global counter
        config = json.load(file)
        articles_categorized = {}
        article_urls_categorized = {}
        for source, details in config.items():
            recent_news = await get_recent_news_by_corporation(conn_params_production, details['corporation_id'])
            print("getting the news ________________________________ " + source)
            scraper = load_scraper(details)
            article_urls_categorized = scraper.fetch_article_urls_all_categories(details["category_path"])

            max_workers = 10
            for category, article_urls in article_urls_categorized.items():
                print(f"\n***{category}***")
                category_start_time = time.time()  # Start timing for this category
                articles_categorized[category] = []
                number_of_articles_scraped = 0
                total_number_of_links = len(article_urls)
                counter = 0
                
                with ThreadPoolExecutor(max_workers=max_workers) as executor:
                    future_to_url = {}
                    for article_url in article_urls:
                        url = article_url['url']
                        future = executor.submit(fetch_and_scrape, scraper, url, recent_news)
                        future_to_url[future] = url

                    for future in as_completed(future_to_url):
                        article_data = future.result()
                        if article_data:
                            number_of_articles_scraped += 1
                            articles_categorized[category].append(article_data)

                print(f"scraping results: scraped-{number_of_articles_scraped} existed-{counter} total-{total_number_of_links}")
                # Create a list to hold all tasks
                tasks = []
                for article in articles_categorized[category]:
                    task = insert_article_and_category(conn_params_production, article, details['corporation_id'], details['corporation_name'], details['corporation_logo'], details['category_path'][category])
                    tasks.append(task)

                # Wait for all tasks to complete
                await asyncio.gather(*tasks)
                
                category_elapsed = time.time() - category_start_time
                print(f"{category}: added {len(articles_categorized[category])} news - {category_elapsed:.2f} seconds.")

        with open('articles.json', 'w') as outfile:
            json.dump(articles_categorized, outfile, indent=4, default=datetime_converter)

    total_elapsed = time.time() - start_time
    print(f"Total execution time: {total_elapsed:.2f} seconds.")
 
def scrape_one():
    article_url = 'https://abcnews.go.com/Entertainment/wireStory/sin-city-city-angels-building-starts-high-speed-109484497'
    with open('config.json') as file:
        config = json.load(file)
        scraper = load_scraper(config["ABCNews"])
        article_data = scraper.scrape_article(article_url)
        result = scraper.fetch_article_urls_one_category("/Sports")
        #print(article_data)
        
        try:
            with open('articles.json', 'w') as outfile:
                json.dump(result, outfile, indent=4, default=datetime_converter)
        except TypeError as e:
            print(f"Error writing JSON: {e}")

if __name__ == '__main__':
    asyncio.run(parallel_main())
    #scrape_one()