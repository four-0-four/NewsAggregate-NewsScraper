from data.newsData import insert_news_affiliate
from newsdataapi import NewsDataApiClient
import json
import sys
from pathlib import Path
import asyncio

# Locate the directory of the current script
current_script_path = Path(__file__).parent.absolute()

# Determine the path to the directory where the target module is located
# Assuming the 'data' directory is at the root of your project, adjust as necessary
project_root = current_script_path.parent.parent
target_module_path = project_root / 'data'

# Add the target module's directory to sys.path
sys.path.append(str(target_module_path))

# Now you can import your module
from newsService import add_news_to_database

# Define an async main function to call get_news_sources
async def get_news_given_url_and_save(url):
    # API key authorization, Initialize the client with your API key
    api = NewsDataApiClient(apikey="pub_38741469a1fcf444f2b92bb3d3d178a0951e8")
    print("about to get news")

    page=None
    reponse = None
    while True:
        response = api.news_api(page = page, domainurl=url, timeframe=24)
        
        if response.get('status') != 'success':
            print("Failed to fetch news: ", response.get('message'))
            break
        
        # Save the news data to the database
        for news in response.get('results'):
            add_news_to_database(news.get('title'), news.get('description'), news.get('content'), news.get('publishedDate'), news.get('url'), news.get('image_url'))
        
        page = response.get('nextPage',None)
        if not page:    
            break

# Run the main function using asyncio.run() if your Python version is 3.7+
if __name__ == "__main__":
    urls = ["cbc.ca","nationalpost.com"]
    for url in urls:
        asyncio.run(get_news_given_url_and_save(url))