# Import necessary modules
import datetime
from Categorizer import predict_category
from newsData import does_news_has_already_category, fetch_news_by_title, insert_news_affiliate, insert_news_category
from newsData import insert_media, insert_news, check_news_title_exists, insert_news_media
import aiohttp

from stablediffusion import get_news_summary
            
            
async def add_news_to_database(conn_params, corporationId, title, content, pubDate, url,image_url, nlp, logging=False):
    if logging:
        print("**********************************************")
    if await check_news_title_exists(conn_params, title):
        if logging:
            print(f"news already exists in the database, {title}")
        news_entry = await fetch_news_by_title(conn_params, title)
    else:
        try:
            if logging:
                print("getting the news summary")
                start_time = datetime.datetime.now()
            longSummary = await get_news_summary(title, content)
            if logging:
                end_time = datetime.datetime.now()  # End timing
                duration = end_time - start_time
                print("got news summary",len(longSummary),"characters long and it took",duration)
            news_entry = await insert_news(conn_params, title, content, longSummary, pubDate)
        except Exception as e:
            print(f"Failed to insert news to database: {e}, {title}")
            return "Failed to insert news"
        
    if logging:
        print("inserting the news", news_entry.get('id'))   
        print("getting the categories for news")
    
    if news_entry == -1:
        print(f"Failed to insert news, {title}")
        return "Failed to insert news"
    
    if logging:
        print("inserting the news affiliate")
    # Insert news affiliate with try-except block
    try:
        await insert_news_affiliate(conn_params, news_entry.get('id'), corporationId, url)
    except Exception as e:
        print(f"Failed to insert affiliate: {e}, {title}")
    
    
    # some news may not have images at all
    if logging:
        print("inserting the news media")
        
    if(image_url):
        try:
            inserted_media = await insert_media(conn_params, image_url)
        except Exception as e:
            print(f"Failed to insert media: {e}")
        
        
        # Insert news media with try-except block
        try:
            await insert_news_media(conn_params, news_entry.get('id'), inserted_media.get('id'))
        except Exception as e:
            print(f"Failed to insert news media: {e}, {title}")
    else:
        print(f"NOTE: No image for {title}")
    
    if logging:
        print("inserting category")
    # Insert news category with try-except block
    
    if not await does_news_has_already_category(conn_params, news_entry.get('id')):
        category = -1
        try:
            category_response = await predict_category(nlp, title+" . "+content)
            category = int(category_response)
        except ValueError:
                # Handle the error (e.g., log it, return an error message, etc.)
                print("Failed to get and convert category")
        
        try:
            await insert_news_category(conn_params, news_entry.get('id'), category)
        except Exception as e:
            print(f"Failed to insert news category: {e}, {title}") 
    else:
        if logging:
            print("news already has category")
            