# Locate the directory of the current script
current_script_path = Path(__file__).parent.absolute()

# Determine the path to the directory where the target module is located
# Assuming the 'data' directory is at the root of your project, adjust as necessary
project_root = current_script_path.parent.parent
target_module_path = project_root / 'data'

# Add the target module's directory to sys.path
sys.path.append(str(target_module_path))

# Now you can import your module
from data.newsData import insert_news_affiliate
from newsData import insert_media, insert_news, check_news_title_exists, insert_news_media


async def add_news_to_database(title, description, content, pubDate, url,image_url):
    print(f"Adding news to database: {title}, {description}, {content}, {pubDate}, {url}")
    if not await check_news_title_exists(title):
        news_entry = await insert_news(title, description, content, pubDate)
        if news_entry != "news already exists":
            await insert_news_affiliate(news_entry.get('id'), 1, url)
            inserted_media = await insert_media(image_url)
            insert_news_media(news_entry.get('id'), inserted_media.get('id'))