import asyncio
from datetime import datetime, timedelta
from typing import List, Optional
import aiomysql
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

conn_params = {
    "host": os.getenv("DATABASE_HOST", "localhost"),
    "port": int(os.getenv("DATABASE_PORT", "3306")),  # Convert port to integer
    "user": os.getenv("DATABASE_USERNAME", "root"),
    "password": os.getenv("DATABASE_PASSWORD", "password"),
    "db": os.getenv("DATABASE_NAME", "newsdb"),
}


async def get_news_sources() -> Optional[dict]:
    async with aiomysql.create_pool(**conn_params) as pool:
        async with pool.acquire() as conn:
            async with conn.cursor(aiomysql.DictCursor) as cur:
                await cur.execute("SELECT * FROM newsCorporations")
                return await cur.fetchall()


async def insert_news(title: str, description: str, content: str, publishedDate: datetime) -> None:
    # Default values for language_id, isInternal, and isPublished are set directly in the SQL query
    insert_query = """
    INSERT INTO news (title, description, content, publishedDate, language_id, isInternal, isPublished, updatedAt)
    VALUES (%s, %s, %s, %s, 16, 0, 0, null);
    """
    if(not await check_news_title_exists(title)):
        try:
            async with aiomysql.create_pool(**conn_params) as pool:
                async with pool.acquire() as conn:
                    async with conn.cursor() as cur:
                        await cur.execute(insert_query, (title, description, content, publishedDate))
                        await conn.commit()
                        inserted_id = cur.lastrowid  # Get the ID of the last inserted row

            # Optionally, fetch the inserted news item by ID to return it
            return await fetch_news_by_id(inserted_id)

        except Exception as e:
            print(f"An error occurred: {e}")
            return {}
    else:
        return "news already exists"
                
                
async def check_news_title_exists(title: str) -> bool:
    query = "SELECT COUNT(*) FROM news WHERE title = %s;"

    async with aiomysql.create_pool(**conn_params) as pool:
        async with pool.acquire() as conn:
            async with conn.cursor() as cur:
                await cur.execute(query, (title,))
                result = await cur.fetchone()
                return result[0] > 0
            
            
async def fetch_news_by_id(news_id: int) -> dict:
    fetch_query = "SELECT * FROM news WHERE id = %s;"
    try:
        async with aiomysql.create_pool(**conn_params) as pool:
            async with pool.acquire() as conn:
                async with conn.cursor() as cur:
                    await cur.execute(fetch_query, (news_id,))
                    news_item = await cur.fetchone()
                    return news_item if news_item else {}
    except Exception as e:
        print(f"Failed to fetch news by ID: {e}")
        return {}            
    
    
async def insert_news_affiliate(news_id: int, newsCorporation_id: int, externalLink: str) -> dict:
    insert_query = """
    INSERT INTO newsAffiliate (news_id, newsCorporation_id, externalLink, createdAt, updatedAt)
    VALUES (%s, %s, %s, NOW(), NOW());
    """
    if(not await check_news_affiliate_exists(news_id, newsCorporation_id)):
        try:
            async with aiomysql.create_pool(**conn_params) as pool:
                async with pool.acquire() as conn:
                    async with conn.cursor() as cur:
                        await cur.execute(insert_query, (news_id, newsCorporation_id, externalLink))
                        await conn.commit()
                        inserted_id = cur.lastrowid  # Assuming an auto-increment ID is present

            # Return the inserted news affiliate item by ID
            return await fetch_news_affiliate_by_id(inserted_id)

        except Exception as e:
            print(f"An error occurred: {e}")
            return {}
    else:
        return "news affiliate already exists"


async def fetch_news_affiliate_by_id(affiliate_id: int) -> dict:
    fetch_query = "SELECT * FROM newsAffiliate WHERE id = %s;"
    try:
        async with aiomysql.create_pool(**conn_params) as pool:
            async with pool.acquire() as conn:
                async with conn.cursor(aiomysql.DictCursor) as cur:
                    await cur.execute(fetch_query, (affiliate_id,))
                    affiliate_item = await cur.fetchone()
                    return affiliate_item if affiliate_item else {}
    except Exception as e:
        print(f"Failed to fetch news affiliate by ID: {e}")
        return {}
    
 
async def check_news_affiliate_exists(news_id: int, newsCorporation_id: int) -> bool:
    query = "SELECT COUNT(*) FROM newsAffiliate WHERE news_id = %s AND newsCorporation_id = %s;"

    async with aiomysql.create_pool(**conn_params) as pool:
        async with pool.acquire() as conn:
            async with conn.cursor() as cur:
                await cur.execute(query, (news_id, newsCorporation_id))
                result = await cur.fetchone()
                return result[0] > 0


async def fetch_media_by_id(media_id: int) -> dict:
    fetch_query = "SELECT * FROM media WHERE id = %s;"
    try:
        async with aiomysql.create_pool(**conn_params) as pool:
            async with pool.acquire() as conn:
                async with conn.cursor(aiomysql.DictCursor) as cur:
                    await cur.execute(fetch_query, (media_id,))
                    media_item = await cur.fetchone()
                    return media_item if media_item else {}
    except Exception as e:
        print(f"Failed to fetch media by ID: {e}")
        return {}


async def fetch_media_by_filename(fileName: str) -> dict:
    fetch_query = "SELECT * FROM media WHERE fileName = %s;"
    try:
        async with aiomysql.create_pool(**conn_params) as pool:
            async with pool.acquire() as conn:
                async with conn.cursor(aiomysql.DictCursor) as cur:
                    await cur.execute(fetch_query, (fileName,))
                    media_item = await cur.fetchone()
                    return media_item if media_item else {}
    except Exception as e:
        print(f"Failed to fetch media by filename: {e}")
        return {}

async def insert_media(fileName: str) -> dict:
    insert_query = """
    INSERT INTO media (createdAt, updatedAt, type, fileName, fileExtension)
    VALUES (NOW(), NOW(), "news image", %s, "url");
    """
    if(not await check_media_exists(fileName)):
        try:
            async with aiomysql.create_pool(**conn_params) as pool:
                async with pool.acquire() as conn:
                    async with conn.cursor() as cur:
                        await cur.execute(insert_query, (fileName))
                        await conn.commit()
                        inserted_id = cur.lastrowid

            # Return the inserted media item by ID
            return await fetch_media_by_id(inserted_id)

        except Exception as e:
            print(f"An error occurred: {e}")
            return {}
    else:
        media = await fetch_media_by_filename(fileName)
        return media if media else "media already exists"
        

async def check_media_exists(fileName: str) -> bool:
    query = "SELECT COUNT(*) FROM media WHERE fileName = %s;"

    async with aiomysql.create_pool(**conn_params) as pool:
        async with pool.acquire() as conn:
            async with conn.cursor() as cur:
                await cur.execute(query, (fileName,))
                result = await cur.fetchone()
                return result[0] > 0
            
       
async def insert_news_media(news_id: int, media_id: int) -> dict:
    insert_query = """
    INSERT INTO newsMedia (news_id, media_id, createdAt, updatedAt)
    VALUES (%s, %s, NOW(), NOW());
    """
    if(not await check_news_media_exists(news_id, media_id)):
        try:
            async with aiomysql.create_pool(**conn_params) as pool:
                async with pool.acquire() as conn:
                    async with conn.cursor() as cur:
                        await cur.execute(insert_query, (news_id, media_id))
                        await conn.commit()
                        inserted_id = cur.lastrowid  # Assuming an auto-increment ID is present
                        
            return {"inserted_id": inserted_id, "news_id": news_id, "media_id": media_id}

        except Exception as e:
            print(f"An error occurred: {e}")
            return {}
    else:
        return "news media already exists"
            
            
async def check_news_media_exists(news_id: int, media_id: int) -> bool:
    query = "SELECT COUNT(*) FROM newsMedia WHERE news_id = %s AND media_id = %s;"

    async with aiomysql.create_pool(**conn_params) as pool:
        async with pool.acquire() as conn:
            async with conn.cursor() as cur:
                await cur.execute(query, (news_id, media_id))
                result = await cur.fetchone()
                return result[0] > 0
            
if __name__ == "__main__":
    # Example data (adjust the datetime values as needed)
    title = "Example News Title"
    description = "This is a short description of the news."
    content = "This is the full content of the news article."
    publishedDate = datetime.now()
    print(asyncio.run(insert_news(title, description, content, publishedDate)))