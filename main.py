import asyncio
from datetime import datetime
import json
import importlib
from concurrent.futures import ThreadPoolExecutor, as_completed
import time
from database import get_recent_news_by_corporation, insert_into_scraper_history, insert_news, insert_news_category
import os
from dotenv import load_dotenv
import aiomysql

pool = None

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

existed_in_db = 0
num_news_with_full_attributes = 0
num_news_invalidated = 0
num_news_scraped = 0

def fetch_and_scrape(scraper, url, recent_news):
    global existed_in_db
    global num_news_invalidated
    global num_news_scraped
    global num_news_with_full_attributes
    
    if url in recent_news:
        existed_in_db += 1
        return None
    
    article_data = scraper.scrape_article(url)
    if not article_data:
        num_news_invalidated += 1
    else:
        num_news_scraped += 1
        if len(article_data['title']) > 10 and len(article_data['content']) > 100 and article_data['date'] and article_data['image_url'] and  len(article_data['image_url']) > 10:
            num_news_with_full_attributes += 1
        
    return article_data

async def insert_article_and_category(pool, article, corporation_id, corporation_name, corporation_logo, category_id):
    news = await insert_news(
        pool,
        title=article['title'],
        content=article['content'],
        publishedDate=article['date'],
        externalNewsURL=article['url'],
        imageURL=article['image_url'],
        corporationID=corporation_id,
        corporationName=corporation_name,
        corporationLogo=corporation_logo
    )
    #print(f"inserted {news.get("id")}")
    if category_id != -1 and news.get("id"):
        await insert_news_category(pool, news.get("id"), category_id)

async def scrape_source_given_details(source, details):
    global pool
    global num_news_with_full_attributes
    global num_news_invalidated
    global num_news_scraped
    global existed_in_db
    
    start_time = time.time()  # Start timing for overall execution
    articles_categorized = {}
    article_urls_categorized = {}
    recent_news = await get_recent_news_by_corporation(pool, details['corporation_id'])
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
        existed_in_db = 0
        num_news_scraped = 0
        num_news_invalidated = 0
        num_news_with_full_attributes = 0
        
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

        print(f"scraping results: scraped-{number_of_articles_scraped} existed-{existed_in_db} total-{total_number_of_links}")
        # Create a list to hold all tasks
        #try:
        #    with open('articles.json', 'w') as outfile:
        #        json.dump(articles_categorized, outfile, indent=4, default=datetime_converter)
        #except TypeError as e:
        #    print(f"Error writing JSON: {e}")
            
        tasks = []
        for article in articles_categorized[category]:
            task = insert_article_and_category(pool, article, details['corporation_id'], details['corporation_name'], details['corporation_logo'], details['category_path'][category])
            tasks.append(task)

        # Wait for all tasks to complete
        await asyncio.gather(*tasks)
        
        category_elapsed = time.time() - category_start_time
        print(f"{category}: added {len(articles_categorized[category])} news - {category_elapsed:.2f} seconds.")
        
        #insert into scraper_history the results of the scraping
        data = {
            'corporation_ID': details['corporation_id'],
            'corporation_category': category,
            'scraper_time': datetime.now(),
            'num_of_links': total_number_of_links,
            'num_of_news_scraped': num_news_scraped,
            'num_of_news_in_db': existed_in_db,
            'num_of_news_with_all_attributes': num_news_with_full_attributes,
            'num_of_news_invalidated': num_news_invalidated,
            'homepage_test': True,
            'topicpage_test': True,
            'newspage_test': True
        }
        
        await insert_into_scraper_history(pool, data)
        
    total_elapsed = time.time() - start_time
    print(f"Total execution time: {total_elapsed:.2f} seconds.")

#with open('articles.json', 'w') as outfile:
#    json.dump(articles_categorized, outfile, indent=4, default=datetime_converter)


async def parallel_main():
    global pool
    pool = await aiomysql.create_pool(**conn_params_production)
    try:
        with open('config.json') as file:
            config = json.load(file)
            for source, details in config.items():
                await scrape_source_given_details(source, details)
            print("All scraping done.")
    finally:
        pool.close()
        await pool.wait_closed()
    
 
async def parallel_one_news_source(newsSource):
    global pool
    pool = await aiomysql.create_pool(**conn_params_production)
    try:
        with open('config.json') as file:
            config = json.load(file)
            source = newsSource
            details = config[source]
            await scrape_source_given_details(source, details)
            print(f"Scraping {source} done.")
    finally:
        pool.close()
        await pool.wait_closed()
 
def scrape_urls_one_category_given_news_source(news_source, write_to_file=False):
    with open('config.json') as file:
        config = json.load(file)
        scraper = load_scraper(config[news_source])
        result = scraper.fetch_article_urls_one_category("/")
        #print(article_data)
        
        if write_to_file:
            try:
                with open('articles.json', 'w') as outfile:
                    json.dump(result, outfile, indent=4, default=datetime_converter)
            except TypeError as e:
                print(f"Error writing JSON: {e}")
                
        return result


async def scrape_article_given_url(news_source, article_url):
    with open('config.json') as file:
        config = json.load(file)
        scraper = load_scraper(config[news_source])
        article_data = scraper.scrape_article(article_url)
        return article_data

if __name__ == '__main__':
    asyncio.run(parallel_main())
    
    
    #asyncio.run(parallel_one_news_source())
    #asyncio.run(scrape_article_given_url())
    #scrape_urls_one_category_given_news_source()