from datetime import datetime
from scraper.news_scraper import NewsScraper
import pytz

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
        image_selector = ('figure',['embed'], 'src')
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

    def scrape_image(self, soup):
        figure_tag = soup.find(self.image_selector[0], class_=self.image_selector[1])
        image_tag = figure_tag.find('link', attrs={'as':'image'})
        if image_tag:
            image_url = image_tag['href']
            return image_url   
        
        # If no image found, look for images in the article
#        embed_images = soup.select('figure.embed img')
#        if embed_images:
#            return [img['src'] for img in embed_images]
#        else:
#            print("No images found.")
#            return None
    
    def scrape_description(self, soup):
        #getting the content of the article
        for content__body in self.content_selector[1]:
            content_tags = soup.find(self.content_selector[0], class_=content__body)
            p_tags = content_tags.find_all('p')
            content = ""
            for p_tag in p_tags:
                p = p_tag.get_text(separator=' ', strip=True)
                content += p
        return content if content else None          


#    # Get the datetime from the <time> text
#    def scrape_date(self, soup):
#        datetime_text = soup.find('time').string.strip()

#        date_parts = datetime_text.split("/")
#        if len(date_parts) == 2:
#            date_str, time_str = date_parts
#            datetime_text = f"{date_str.strip()} {time_str.strip()}"
#            # Remove "Updated on:","EDT"
#            datetime_str = datetime_text.replace("Updated on:", "").replace("EDT", "").strip()
              
#            # Convert to a datetime object
#            datetime_object = datetime.strptime(datetime_str, self.date_format)
            
            # Convert timezone to UTC    
#            timezone = pytz.timezone('America/New_York')
#            utc_datetime = timezone.localize(datetime_object)
#            utc_date = utc_datetime.astimezone(pytz.utc)
#            return utc_date
