import asyncio
import datetime
from logging import exception

# Now, import your modules after adding their directories to sys.path
from Categorizer import predict_category
from newsData import get_news_source_urls, insert_news_affiliate
from newsService import add_news_to_database
from newsdataapi import NewsDataApiClient
from dotenv import load_dotenv
import spacy
import os
import json

from stablediffusion import get_news_summary

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

async def get_news_for_one_corporation_from_newsdataio(url, nlp):
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
            category = -1
            try:
                print(news.get('title'))
                category_response = await predict_category(nlp, news.get('title') + " . " + news.get('content'))
                if category_response is not None:
                    category = int(category_response)
                else:
                    news_item = {
                        "title": news.get('title'),
                        "content": news.get('content'),
                        "category": category
                    }

                    # Append each news item to the file immediately in JSON Lines format
                    with open('news_data.jsonl', 'a') as json_file:
                        json_file.write(json.dumps(news_item) + '\n')
            except Exception as e:  # Corrected to Exception
                # Handle the error (e.g., log it, return an error message, etc.)
                print(f"Failed to get and convert category due to an error: {e}")
                news_item = {
                    "title": news.get('title'),
                    "content": news.get('content'),
                    "category": category
                }

                # Append each news item to the file immediately in JSON Lines format
                with open('news_data.jsonl', 'a') as json_file:
                    json_file.write(json.dumps(news_item) + '\n')
            print("category: ", category)
            
            longSummary = await get_news_summary(news.get('title'), news.get('content'))
            print("longSummary: ", len(longSummary))
        page = response.get('nextPage',None)
        if not page:    
            break
        
    print(f"**********Saved {count} news articles from {url}")

# Define an async main function to call get_news_sources
async def get_news_given_url_and_save(conn_params, url, corporationId, nlp, logging=False):
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
                if logging:
                    start_time = datetime.datetime.now()  # Start timing
                await add_news_to_database(conn_params, corporationId, news.get('title'), news.get('content'), news.get('pubDate'), news.get('link'), news.get('image_url'), nlp, logging)
                if logging:
                    end_time = datetime.datetime.now()  # End timing
                    duration = end_time - start_time
                    print(f"Time taken to save news: {duration}")
            except Exception as e:
                print(f"Failed to save news: {e}, {news.get('title')}")
        
        page = response.get('nextPage',None)
        if not page:    
            break
    if logging:
        print(f"**********Saved {count} news articles from {url}")


async def news_for_all_urls(conn_params,nlp, logging=False):
    corporationUrls = await get_news_source_urls(conn_params)

    for corporationUrl in corporationUrls:
        if(corporationUrl["url"] == None or corporationUrl["api-newsdata.io"] == 0):
            continue
        # Remove 'https://www.' from the URL
        clean_url = corporationUrl["url"].replace("https://www.", "")
        corporationId = corporationUrl["CorporationID"]
        try:
            await get_news_given_url_and_save(conn_params, clean_url, corporationId, nlp, logging)
        except Exception as e:
            print(f"Failed to get news for {clean_url}: {e}")

# Run the main function using asyncio.run() if your Python version is 3.7+
if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    print("loading custom spacy model")
    nlp = spacy.load("custom_model_artifacts")
    #loop.run_until_complete(get_news_for_one_corporation_from_newsdataio("nationalpost.com", nlp))
    

    environment = os.getenv("ENV","stage")
    if environment == "stage" or environment == "dev":
        print("############################################")
        print("Running in stage environment")
        print("############################################")
        loop.run_until_complete(news_for_all_urls(conn_params_stage,nlp, True))
    else:
        print("############################################")
        print("Running in production environment")
        print("############################################")
        loop.run_until_complete(news_for_all_urls(conn_params_production,nlp, True))

    