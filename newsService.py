# Import necessary modules
from newsData import fetch_news_by_title, insert_news_affiliate
from newsData import insert_media, insert_news, check_news_title_exists, insert_news_media
 
            
async def add_news_to_database(conn_params, corporationId, title, content, pubDate, url,image_url, logging=False):
    if logging:
        print("**********************************************")
    if await check_news_title_exists(conn_params, title):
        if logging:
            print(f"news already exists in the database, {title}")
        news_entry = await fetch_news_by_title(conn_params, title)
    else:
        try:
            news_entry = await insert_news(conn_params, title, content, pubDate)
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
        
    return news_entry.get('id')
            