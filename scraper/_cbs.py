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
        image_selector = ('body','figure',['is-video','embed'], 'src')
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
        img_tags = soup.find_all(self.image_selector[0], class_=self.image_selector[2])

        for img_tag in img_tags:
            # Look for preview-image
            preview_image = img_tag.find('img', class_='body--preview-image')
            if preview_image:
                img_url = preview_image['src']
                return img_url
            else:
                # If no preview-image, look for the div with slot="poster"
                div_tag = img_tag.find('div', attrs={'slot': 'poster'})
                if div_tag:
                    img_url = div_tag.find('img')['src']
                    return img_url
    
        # If no image found, look for images in the article
        embed_images = soup.select('figure.embed img')
        if embed_images:
            return [img['src'] for img in embed_images]
        else:
            print("No images found.")
            return None




        
