import asyncio
from datetime import datetime, timedelta
import os
from typing import List, Optional
import aiomysql


async def get_news_sources(pool) -> Optional[dict]:
    async with pool.acquire() as conn:
        async with conn.cursor(aiomysql.DictCursor) as cur:
            await cur.execute("SELECT * FROM newsCorporations")
            return await cur.fetchall()
            
            

async def get_news_source_urls(pool) -> Optional[dict]:
    POD = os.getenv("POD", 3)
    print(f"POD is {POD}")
    async with pool.acquire() as conn:
        async with conn.cursor(aiomysql.DictCursor) as cur:
            await cur.execute("SELECT * FROM newsCorporationsURLs where `api-newsdata.io-pod` = %s", (POD,))
            return await cur.fetchall()


async def insert_into_scraper_history(pool, data):
    query = """
    INSERT INTO scraper_history (
        corporation_ID, corporation_category, scraper_time, 
        num_of_links, num_of_news_scraped, num_of_news_in_db, 
        num_of_news_with_all_attributes, num_of_news_invalidated, 
        homepage_test, topicpage_test, newspage_test
    ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
    """
    
    try:
        async with pool.acquire() as conn:
            async with conn.cursor() as cur:
                result = await cur.execute(query, (
                    data['corporation_ID'], data['corporation_category'], data['scraper_time'],
                    data['num_of_links'], data['num_of_news_scraped'], data['num_of_news_in_db'],
                    data['num_of_news_with_all_attributes'], data['num_of_news_invalidated'],
                    data['homepage_test'], data['topicpage_test'], data['newspage_test']
                ))
                await conn.commit()
                #print(f"Rows affected: {result}")  # This will print the number of rows affected by the insert statement
    except Exception as e:
        print(f"An error occurred: {e}")


async def insert_news(pool, title: str, content: str, publishedDate: datetime, externalNewsURL: str, imageURL: str, corporationID: int, corporationName: str, corporationLogo: str) -> None:
    # Default values for language_id, isInternal, and isPublished are set directly in the SQL query
    insert_query = """
    INSERT INTO news (title, content, publishedDate, language_id, isInternal, ProcessedForIdentity, summarized, mainImage, corporationName, corporationLogo, newsExternalLink, corporationID)
    VALUES (%s, %s, %s, 16, 0, 0, 0, %s, %s, %s, %s, %s);
    """
    if(not publishedDate):
        print(f"ERROR: published date is null. not adding the news. title is: {title}, published date is: {publishedDate}")
        return -1
    
    if(not await check_news_exists(pool, title, externalNewsURL)):
        try:
            async with pool.acquire() as conn:
                async with conn.cursor(aiomysql.DictCursor) as cur:
                    await cur.execute(insert_query, (title, content, publishedDate, imageURL, corporationName, corporationLogo, externalNewsURL, corporationID))
                    await conn.commit()
                    inserted_id = cur.lastrowid  # Get the ID of the last inserted row

            # Optionally, fetch the inserted news item by ID to return it
            return await fetch_news_by_id(pool, inserted_id)

        except Exception as e:
            print(f"An error occurred: {e}")
            return {}
    else:
        return await fetch_news_by_title(pool, title)
    
    
async def insert_summary_for_news(pool, news_id: int, summary: str) -> None:
    """
    Updates the news item with the given news_id, setting its summary and marking it as summarized.
    
    :param pool: Database connection parameters.
    :param news_id: The ID of the news item to update.
    :param summary: The summary to insert for the news item.
    """
    update_query = """
    UPDATE news
    SET longSummary = %s, summarized = 1
    WHERE id = %s;
    """

    try:
        async with pool.acquire() as conn:
            async with conn.cursor() as cur:
                await cur.execute(update_query, (summary, news_id))
                await conn.commit()

    except Exception as e:
        print(f"An error occurred while updating news summary: {e}")
        
        
async def check_that_news_is_categorized(pool, news_id: int) -> None:
    """
    Updates the news item with the given news_id, setting its summary and marking it as summarized.
    
    :param pool: Database connection parameters.
    :param news_id: The ID of the news item to update.
    :param summary: The summary to insert for the news item.
    """
    update_query = """
    UPDATE news
    SET ProcessedForIdentity = 1
    WHERE id = %s;
    """

    try:
        async with pool.acquire() as conn:
            async with conn.cursor() as cur:
                await cur.execute(update_query, (news_id, ))
                await conn.commit()

    except Exception as e:
        print(f"An error occurred while updating news summary: {e}")
                
                
async def check_news_exists(pool, title: str, externalLink: str) -> bool:
    query = "SELECT COUNT(*) AS count FROM news WHERE title = %s OR newsExternalLink = %s;"

    async with pool.acquire() as conn:
        async with conn.cursor(aiomysql.DictCursor) as cur:
            await cur.execute(query, (title, externalLink))
            result = await cur.fetchone()
            return result['count'] > 0
  
async def fetch_news_by_title(pool, title: int) -> dict:
    fetch_query = "SELECT * FROM news WHERE title = %s;"
    try:
        async with pool.acquire() as conn:
            async with conn.cursor(aiomysql.DictCursor) as cur:
                await cur.execute(fetch_query, (title,))
                news_item = await cur.fetchone()
                return news_item if news_item else {}
    except Exception as e:
        print(f"Failed to fetch news by ID: {e}")
        return {}   
            
async def fetch_news_by_id(pool, news_id: int) -> dict:
    fetch_query = "SELECT * FROM news WHERE id = %s;"
    try:
        async with pool.acquire() as conn:
            async with conn.cursor(aiomysql.DictCursor) as cur:
                await cur.execute(fetch_query, (news_id,))
                news_item = await cur.fetchone()
                return news_item if news_item else {}
    except Exception as e:
        print(f"Failed to fetch news by ID: {e}")
        return {}            


async def fetch_corporation(pool, newsCorporation_id: int) -> dict:
    fetch_query = "SELECT * FROM newsCorporations WHERE id = %s;"
    try:
        async with pool.acquire() as conn:
            async with conn.cursor(aiomysql.DictCursor) as cur:
                await cur.execute(fetch_query, (newsCorporation_id))
                affiliate_item = await cur.fetchone()
                return affiliate_item if affiliate_item else {}
    except Exception as e:
        print(f"Failed to fetch corporation by ID: {e}")
        return {}


async def fetch_media_by_id(pool, media_id: int) -> dict:
    fetch_query = "SELECT * FROM media WHERE id = %s;"
    try:
        async with pool.acquire() as conn:
            async with conn.cursor(aiomysql.DictCursor) as cur:
                await cur.execute(fetch_query, (media_id,))
                media_item = await cur.fetchone()
                return media_item if media_item else {}
    except Exception as e:
        print(f"Failed to fetch media by ID: {e}")
        return {}


async def fetch_media_by_filename(pool, fileName: str) -> dict:
    fetch_query = "SELECT * FROM media WHERE fileName = %s;"
    try:
        async with pool.acquire() as conn:
            async with conn.cursor(aiomysql.DictCursor) as cur:
                await cur.execute(fetch_query, (fileName,))
                media_item = await cur.fetchone()
                return media_item if media_item else {}
    except Exception as e:
        print(f"Failed to fetch media by filename: {e}")
        return {}

async def insert_media(pool, fileName: str) -> dict:
    insert_query = """
    INSERT INTO media (createdAt, updatedAt, type, fileName, fileExtension)
    VALUES (NOW(), NOW(), 'news image', %s, 'url');
    """
    if(not await check_media_exists(pool, fileName)):
        try:
            async with pool.acquire() as conn:
                async with conn.cursor(aiomysql.DictCursor) as cur:
                    await cur.execute(insert_query, (fileName,))
                    await conn.commit()
                    inserted_id = cur.lastrowid

            # Return the inserted media item by ID
            return await fetch_media_by_id(pool, inserted_id)

        except Exception as e:
            print(f"An error occurred: {e}")
            return {}
    else:
        media = await fetch_media_by_filename(pool, fileName)
        return media if media else "media already exists"
        

async def check_media_exists(pool, fileName: str) -> bool:
    query = "SELECT COUNT(*) FROM media WHERE fileName = %s;"

    async with pool.acquire() as conn:
        async with conn.cursor() as cur:
            await cur.execute(query, (fileName,))
            result = await cur.fetchone()
            return result[0] > 0
            
       
async def insert_news_media(pool, news_id: int, media_id: int) -> dict:
    insert_query = """
    INSERT INTO newsMedia (news_id, media_id, createdAt, updatedAt)
    VALUES (%s, %s, NOW(), NOW());
    """
    if(not await check_news_media_exists(pool, news_id, media_id)):
        try:
            async with pool.acquire() as conn:
                async with conn.cursor(aiomysql.DictCursor) as cur:
                    await cur.execute(insert_query, (news_id, media_id))
                    await conn.commit()
                        
            return {"news_id": news_id, "media_id": media_id}

        except Exception as e:
            print(f"An error occurred: {e}")
            return {}
    else:
        return "news media already exists"
            
            
async def check_news_media_exists(pool, news_id: int, media_id: int) -> bool:
    query = "SELECT COUNT(*) FROM newsMedia WHERE news_id = %s AND media_id = %s;"

    async with pool.acquire() as conn:
        async with conn.cursor() as cur:
            await cur.execute(query, (news_id, media_id))
            result = await cur.fetchone()
            return result[0] > 0
            
            
async def insert_news_category(pool, news_id: int, category_id: int) -> dict:
    insert_query = """
    INSERT INTO newsTopic (newsID, topicID, topicType)
    VALUES (%s, %s, 'CATEGORY');
    """
    if(not await check_news_category_exists(pool, news_id, category_id)):
        try:
            async with pool.acquire() as conn:
                async with conn.cursor(aiomysql.DictCursor) as cur:
                    await cur.execute(insert_query, (news_id, category_id))
                    await conn.commit()
                        
            return {"news_id": news_id, "category_id": category_id}

        except Exception as e:
            print(f"An error occurred: {e}")
            return {}
    else:
        return "news category already exists"
 

async def get_recent_news_by_corporation(pool, corporation_id: int):
    # SQL query to select news from the last 36 hours for a given corporation_id
    fetch_query = """
    SELECT newsExternalLink
    FROM news
    WHERE corporationID = %s AND publishedDate > %s;
    """

    # Calculate the time 36 hours ago from the current time
    thirty_six_hours_ago = datetime.utcnow() - timedelta(hours=36)

    try:
        async with pool.acquire() as conn:
            async with conn.cursor(aiomysql.DictCursor) as cur:
                # Execute the SQL query with parameters
                await cur.execute(fetch_query, (corporation_id, thirty_six_hours_ago))
                # Fetch all records that match the query
                news_records = await cur.fetchall()
                # Extract URLs from each record
                url_list = [record['newsExternalLink'] for record in news_records]
                return url_list
    except Exception as e:
        print(f"An error occurred: {e}")
        return []           
            
async def check_news_category_exists(pool, news_id: int, category_id: int) -> bool:
    query = "SELECT COUNT(*) FROM newsTopic WHERE newsID = %s AND topicID = %s and topicType = 'CATEGORY';"

    async with pool.acquire() as conn:
        async with conn.cursor() as cur:
            await cur.execute(query, (news_id, category_id,))
            result = await cur.fetchone()
            return result[0] > 0
            
            
async def does_news_has_already_category(pool, news_id: int) -> bool:
    query = "SELECT COUNT(*) FROM newsTopic WHERE newsID = %s and topicType = 'CATEGORY';"

    async with pool.acquire() as conn:
        async with conn.cursor() as cur:
            await cur.execute(query, (news_id,))
            result = await cur.fetchone()
            return result[0] > 0