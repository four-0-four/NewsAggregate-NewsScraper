import asyncio

# Now, import your modules after adding their directories to sys.path
from newsData import get_news_source_urls, insert_news_affiliate
from newsService import add_news_to_database
from newsdataapi import NewsDataApiClient
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

conn_params_stage = {
    "host": os.getenv("DATABASE_HOST_STAGE", "localhost"),
    "port": int(os.getenv("DATABASE_PORT_STAGE", "3306")),  # Convert port to integer
    "user": os.getenv("DATABASE_USERNAME_STAGE", "root"),
    "password": os.getenv("DATABASE_PASSWORD_STAGE", "password"),
    "db": os.getenv("DATABASE_NAME_STAGE", "newsdb"),
}


conn_params_production = {
    "host": os.getenv("DATABASE_HOST_PRODUCTION", "localhost"),
    "port": int(os.getenv("DATABASE_PORT_PRODUCTION", "3306")),  # Convert port to integer
    "user": os.getenv("DATABASE_USERNAME_PRODUCTION", "root"),
    "password": os.getenv("DATABASE_PASSWORD_PRODUCTION", "password"),
    "db": os.getenv("DATABASE_NAME_PRODUCTION", "newsdb"),
}

# Define an async main function to call get_news_sources
async def get_news_given_url_and_save(conn_params, url, corporationId):
    # API key authorization, Initialize the client with your API key
    api = NewsDataApiClient(apikey="pub_38741469a1fcf444f2b92bb3d3d178a0951e8")
    print("about to get news")

    page=None
    reponse = None
    count = 0
    while True:
        response = api.news_api(page = page, domainurl=url, timeframe=8)
        
        if response.get('status') != 'success':
            print("Failed to fetch news: ", response.get('message'))
            break
        # Save the news data to the database
        for news in response.get('results'):
            count += 1
            try:
                await add_news_to_database(conn_params, corporationId, news.get('title'), news.get('description'), news.get('content'), news.get('pubDate'), news.get('link'), news.get('image_url'))
            except Exception as e:
                print(f"Failed to save news: {e}, {news.get('title')}")
        
        page = response.get('nextPage',None)
        if not page:    
            break
    print(f"**********Saved {count} news articles from {url}")


async def news_for_all_urls(conn_params):
    corporationUrls = await get_news_source_urls(conn_params)

    for corporationUrl in corporationUrls:
        if(corporationUrl["url"] == None or corporationUrl["api-newsdata.io"] == 0):
            continue
        # Remove 'https://www.' from the URL
        clean_url = corporationUrl["url"].replace("https://www.", "")
        corporationId = corporationUrl["CorporationID"]
        try:
            await get_news_given_url_and_save(conn_params, clean_url, corporationId)
        except Exception as e:
            print(f"Failed to get news for {clean_url}: {e}")

# Run the main function using asyncio.run() if your Python version is 3.7+
if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    environment = os.getenv("ENV","stage")
    if environment == "stage" or environment == "dev":
        print("############################################")
        print("Running in stage environment")
        print("############################################")
        loop.run_until_complete(news_for_all_urls(conn_params_stage))
    else:
        print("############################################")
        print("Running in production environment")
        print("############################################")
        loop.run_until_complete(news_for_all_urls(conn_params_production))