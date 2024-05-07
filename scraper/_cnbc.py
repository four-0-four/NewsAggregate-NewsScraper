from datetime import datetime
from scraper.news_scraper import NewsScraper
import re

class CNBCNewsScraper(NewsScraper):
    def __init__(self, base_url, urls_blacklist):
        
        #(css_to_url, css_to_title)
        article_url_css_selector = [
            ('a', 'a'),
            ('div.TrayCard-cardContainer a', 'div.TrayCard-cardContainer .TrayCard-title')
        ]
        
        title_selector = ('h1',['ArticleHeader-headline'])
        date_selector = ('time',['[data-testid="published-timestamp"]'])
        date_format = '%B %d, %Y, %I:%M %p'
        image_selector = ('div',['MediaPlaceholder', 'InlineImage GpQCA lZur asrEW'], 'src')
        content_selector = ('div',['xvlfx ZRifP TKoO eaKKC bOdfO'])
        super().__init__(base_url, article_url_css_selector, title_selector, date_selector, date_format, image_selector, content_selector, urls_blacklist)
        
    def check_article_url(self,href):
        print("href:", href)
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
            #print("date_tag:",date_tag)
            if(date_tag and 'datetime' in date_tag.attrs):
                
                datetime_str = date_tag['datetime'] if date_tag else None
                if datetime_str: 
                    date_object = datetime.fromisoformat(datetime_str.rstrip('Z'))
                    return date_object
        
        return None