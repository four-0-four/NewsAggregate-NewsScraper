from datetime import datetime, timezone
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
    
    def scrape_image(self, soup):
        #getting the image of the article
        image_url = None
        for image_class in self.image_selector[1]:
            print("image_class:", image_class)
            image_tags = soup.find_all(self.image_selector[0], class_=image_class)
            print("image_tags:", image_tags)
            for image_tag in image_tags:
                print("image_tag:", image_tag)
                if image_tag and image_tag.find('img') and self.image_selector[2] in image_tag.find('img').attrs:
                    image_url = image_tag.find('img')[self.image_selector[2]]
                    print("image_url:", image_url)
                
                #check if image_url starts with http
                if image_url and not image_url.startswith('http'):
                    image_url = None
                
                if image_url and image_url.startswith('http'):
                    return image_url
        return image_url