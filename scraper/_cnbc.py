from datetime import datetime, timezone
from scraper.news_scraper import NewsScraper
import re
import asyncio
import nest_asyncio
from playwright.async_api import async_playwright
from bs4 import BeautifulSoup
import requests
import json

nest_asyncio.apply()
class CNBCNewsScraper(NewsScraper):
    def __init__(self, base_url, urls_blacklist):
        
        #(css_to_url, css_to_title)
        article_url_css_selector = [
            ('a', 'a'),
            ('div.TrayCard-cardContainer a', 'div.TrayCard-cardContainer .TrayCard-title')
        ]
        
        title_selector = ('h1',['ArticleHeader-headline', 'LiveBlogHeader-headline'])
        date_selector = ('time',[''])
        date_format = '%B %d, %Y, %I:%M %p'
        image_selector = ('div',['InlineImage-imagePlaceholder', 'InlineVideo-inlineThumbnailContainer'], 'src')
        content_selector = ('div',['group'])
        super().__init__(base_url, article_url_css_selector, title_selector, date_selector, date_format, image_selector, content_selector, urls_blacklist)
    
    def check_article_url(self,href):
        if(href.startswith(self.base_url)):
            full_link = href
        elif(href.startswith("/")):
            full_link = self.base_url + href
        else:
            return None
        
        # Regex to match the URL pattern: base_url followed by /year/month/day/
        # This pattern assumes year as four digits, month as 1 or 2 digits, and day as 1 or 2 digits
        pattern = re.escape(self.base_url) + r'\/(\d{4})\/(\d{1,2})\/(\d{1,2})\/'
        if not re.match(pattern, full_link) and not href.startswith(self.base_url+"/select/"):
            return None
        
        is_url_blacklisted = False
        #check that the href not in urls_blacklist
        for url_blacklist in self.urls_blacklist:
            if url_blacklist in full_link:
                is_url_blacklisted = True
                break
        
        if is_url_blacklisted:
            return None
        
        return full_link
    
    def scrape_date(self, soup):
        #getting the date of the article
        for date_class in self.date_selector[1]:
            date_tag = soup.find(self.date_selector[0], class_=date_class)
            if(date_tag and 'datetime' in date_tag.attrs):
                
                datetime_str = date_tag['datetime'] if date_tag else None
                if datetime_str: 
                    date_object = datetime.fromisoformat(datetime_str.rstrip('Z')).replace(tzinfo=timezone.utc)
                    return date_object
        
        return None
    
    def scrape_description(self, soup):
        #getting the content of the article
        content = ""
        for content_class in self.content_selector[1]:
            content_tags = soup.find_all(self.content_selector[0], class_=content_class)
            for content_tag in content_tags:
                if(content_tag):
                    content_section = content_tag.get_text(separator=' ', strip=True)
                
                    #check the content has certain length
                    if content_section and len(content_section) < 100:
                        continue
                    
                    content += " " + content_section
            
        return content


    def extract_json_data(self, script_content):
        # Use regular expression to find the JSON data within the script content
        match = re.search(r'var __CNBC_META_DATA\s*=\s*({.*?});', script_content)
        string_json = match.group(1)
        uncoded_string = string_json.encode('utf-8').decode('unicode_escape')
        json_data = json.loads(uncoded_string)
        return json_data

    def scrape_image(self, soup):
        # Find the script tag containing __CNBC_META_DATA
        script_tag = soup.find('script', text=re.compile(r'var __CNBC_META_DATA'))
        if not script_tag:
            print("Could not find the script tag containing __CNBC_META_DATA")
            return None

        # Extract the script content
        script_content = script_tag.string
        if not script_content:
            print("Script content is empty")
            return None

        # Extract JSON data from the script content
        json_data = self.extract_json_data(script_content)
        if not json_data:
            print("Could not extract JSON data from the script content")
            return None

        
        # Access the promoImage field
        promo_image = json_data.get('promoImage')
        if not promo_image:
            print("promoImage not found in JSON data")
            return None

        image_url = promo_image.get('url')
        if image_url: 
            return image_url
        
        # Iterate through potential image classes to find an image URL
        for image_class in self.image_selector[1]:
            image_tags = soup.find_all(self.image_selector[0], class_=image_class)
            for image_tag in image_tags:
                if image_tag and image_tag.find('img') and self.image_selector[2] in image_tag.find('img').attrs:
                    temp_url = image_tag.find('img')[self.image_selector[2]]
                    if temp_url.startswith('http'):
                        image_url = temp_url
                        break
            if image_url:
                break
        
        return image_url
    
    """###################  Pyppeteer implementation ###################
    async def scrape_image_with_pyppeteer(self, article_url):
        # Initialize image URL to None
        image_url = None
        
        # Start an asynchronous Playwright session
        async with async_playwright() as p:
            browser = await p.chromium.launch()
            page = await browser.new_page()
            
            try:
                # Navigate to the article URL
                await page.goto(article_url)
                # Wait for the image placeholder to load
                await page.wait_for_selector('div.InlineImage-imagePlaceholder', timeout=30000)
                
                # Get the page content and parse it with BeautifulSoup
                soup = BeautifulSoup(await page.content(), "html.parser")
                
                # Iterate through potential image classes to find an image URL
                for image_class in self.image_selector[1]:
                    image_tags = soup.find_all(self.image_selector[0], class_=image_class)
                    for image_tag in image_tags:
                        if image_tag and image_tag.find('img') and self.image_selector[2] in image_tag.find('img').attrs:
                            temp_url = image_tag.find('img')[self.image_selector[2]]
                            if temp_url.startswith('http'):
                                image_url = temp_url
                                break
                    if image_url:
                        break
            except Exception as e:
                # Handle exceptions (e.g., navigation errors, timeouts)
                print("***********************")
                print(article_url)
                print(f"An error occurred: {e}")
            finally:
                # Ensure the browser is closed after processing
                await browser.close()
    
        return image_url

    def scrape_image_sync(self, url):
        loop = asyncio.get_event_loop()
        result = loop.run_until_complete(self.scrape_image_with_pyppeteer(url))
        return result
    """