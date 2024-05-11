from datetime import datetime
import re
import attrs
import pytz
from scraper.news_scraper import NewsScraper

class CBSNewsScraper(NewsScraper):
    def __init__(self, base_url, urls_blacklist):
        
        #(css_to_url, css_to_title)
        article_url_css_selector = [
            ('article.item a', 'article.item a h4'), 
            ('ul.item__related-links', 'ul.item__related-links'),
        ]
        
        title_selector = ('h1',['content__title'])
        date_selector = ('time',[''])
        date_format = '%B %d, %Y %I:%M %p'
        image_selector = ('img',['body--preview-image'], 'src')
        content_selector = ('section',['content__body'])
        super().__init__(base_url, article_url_css_selector, title_selector, date_selector, date_format, image_selector, content_selector, urls_blacklist)
    
    # Get the datetime from time attribute
    def scrape_date(self, soup):
        datetime_value = soup.find('time')['datetime']
        
        # Convert str into datetime_obj
        datetime_object = datetime.strptime(datetime_value, "%Y-%m-%dT%H:%M:%S%z")
        
        # Convert to UTC
        utc_timezone = pytz.timezone('UTC')
        utc_datetime = datetime_object.astimezone(utc_timezone)
        return utc_datetime

    # Get the datetime from the <time> text
    def scrape_date(self, soup):
        datetime_text = soup.find('time').string.strip()

        date_parts = datetime_text.split("/")
        if len(date_parts) == 2:
            date_str, time_str = date_parts
            datetime_text = f"{date_str.strip()} {time_str.strip()}"
            # Remove "Updated on:","EDT"
            datetime_str = datetime_text.replace("Updated on:", "").replace("EDT", "").strip()
              
            # Convert to a datetime object
            datetime_object = datetime.strptime(datetime_str, self.date_format)
            
            # Convert timezone to UTC    
            timezone = pytz.timezone('America/New_York')
            utc_datetime = timezone.localize(datetime_object)
            utc_date = utc_datetime.astimezone(pytz.utc)
            return utc_date

    
    def scrape_image(self, soup):

        image_tag = soup.find('img', class_='body--preview-image')
        if image_tag:
            image_src = image_tag['src']
            print(f"Found image source: {image_src}")
            return image_src
        else:
            print("Image tag not found")
            return None



        
