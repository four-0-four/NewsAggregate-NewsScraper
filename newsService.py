# Import necessary modules
from newsData import fetch_news_by_title, insert_news_affiliate, insert_news_category
from newsData import insert_media, insert_news, check_news_title_exists, insert_news_media
import aiohttp  # Import aiohttp for making async HTTP requests

# New function to make an API call to categorize news
async def categorize_news(text):
    url = "http://159.223.199.115:8000/categorize"
    body = {"text": text}
    async with aiohttp.ClientSession() as session:
        async with session.post(url, json=body) as response:
            if response.status == 200:
                response_data = await response.json()
                return response_data
            else:
                return {"error": "Failed to categorize news"}
            
            
async def add_news_to_database(conn_params, corporationId, title, content, shortSummary, longSummary, pubDate, url,image_url):

    if await check_news_title_exists(conn_params, title):
        print(f"news already exists in the database, {title}")
        news_entry = await fetch_news_by_title(conn_params, title)
    else:
        try:
            news_entry = await insert_news(conn_params, title, content, shortSummary, longSummary, pubDate)
        except Exception as e:
            print(f"Failed to insert news to database: {e}, {title}")
            return "Failed to insert news"
        

    category_response = await categorize_news(title+" . "+content)
    
    try:
        category = category_response["predicted_category"].replace("label_", "")
    except ValueError:
            # Handle the error (e.g., log it, return an error message, etc.)
            print("Failed to get and convert category")
    
    if news_entry == -1:
        print(f"Failed to insert news, {title}")
        return "Failed to insert news"
    
    
    # Insert news affiliate with try-except block
    try:
        await insert_news_affiliate(conn_params, news_entry.get('id'), corporationId, url)
    except Exception as e:
        print(f"Failed to insert affiliate: {e}, {title}")
    
    
    # some news may not have images at all
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
    
    
    # Insert news category with try-except block
    try:
        await insert_news_category(conn_params, news_entry.get('id'), category)
    except Exception as e:
        print(f"Failed to insert news category: {e}, {title}") 
    
            