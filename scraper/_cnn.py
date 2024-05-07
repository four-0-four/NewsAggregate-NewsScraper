from datetime import datetime
from scraper.news_scraper import NewsScraper
import requests
from bs4 import BeautifulSoup
import pytz
import re

class CNNNewsScraper(NewsScraper):
    def __init__(self, base_url, urls_blacklist):
        
        #(css_to_url, css_to_title)
        article_url_css_selector = [
            ('[data-link-type^="article"]', '[data-link-type^="article"] [class$="headline"]'),
            ('[data-link-type^="card"]', '[data-link-type^="card"] [class$="headline"]'),
        ]
        
        title_selector = ('h1',['headline__text'])
        date_selector = ('div',['timestamp'])
        date_format = '%I:%M %p %B %d, %Y'
        image_selector = ('div',['image__container'], 'src')
        content_selector = ('div',['article__content-container'])
        super().__init__(base_url, article_url_css_selector, title_selector, date_selector, date_format, image_selector, content_selector, urls_blacklist)
        
    
    def scrape_date(self, soup):
        # Define the regex pattern for date and time
        date_pattern = re.compile(r"(\d{1,2}:\d{2})\s+(AM|PM)\s+EDT,.*?(\w+\s+\d{1,2},\s+\d{4})", re.DOTALL)
        
        # Search for the date using the specified selectors
        for date_class in self.date_selector[1]:
            date_tag = soup.find(self.date_selector[0], class_=date_class)
            if date_tag:
                # Search within the text of the tag for a date that matches our pattern
                match = date_pattern.search(date_tag.text)
                if match:
                    time = match.group(1)    # Captures '10:37'
                    am_pm = match.group(2)   # Captures 'AM'
                    date = match.group(3)    # Captures 'April 29, 2024
                    datetime_str = f"{time} {am_pm} {date}"
                    # Convert the string to a datetime object
                    date_object = datetime.strptime(datetime_str, self.date_format)
                    # Convert timezone to UTC
                    timezone = pytz.timezone('America/New_York')  # Assuming EDT by default
                    date_object = timezone.localize(date_object)
                    utc_date_object = date_object.astimezone(pytz.utc)
                    return utc_date_object
        return None
    
    def scrape_description(self, soup):
        #getting the content of the article
        for content_class in self.content_selector[1]:
            content = ""
            content_tags = soup.find_all(self.content_selector[0], class_=content_class)
            for content_tag in content_tags:
                if(content_tag):
                    content_section = content_tag.get_text(separator=' ', strip=True)
                
                    #check the content has certain length
                    if content_section and len(content_section) < 100:
                        continue
                    
                    content += " " + content_section
            
        return content
    
    def check_article_url(self,href):
        if(href.startswith("/")):
            full_link = self.base_url + href
        else:
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

    def check_if_article_is_duplicate(self, full_link, href, text):
        #check that we have already added it so we don't add twice
        if (full_link in self.added_urls):
            # Check if the URL exists in article_links and has an empty title
            # or it has less incomplete title
            for article in self.article_links:
                if article['url'] == self.base_url + href and ( not article['title'] or len(article['title']) < len(text) ):
                    self.article_links.remove(article)  # Remove if title is empty
                    break
            else:
                return False
        return True
    