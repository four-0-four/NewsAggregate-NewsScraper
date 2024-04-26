from datetime import datetime
from scraper.news_scraper import NewsScraper
import requests
from bs4 import BeautifulSoup

class NBCNewsScraper(NewsScraper):
    def __init__(self, base_url, urls_blacklist):
        
        #(css_to_url, css_to_title)
        article_url_css_selector = [
            ('.wide-tease-item__wrapper .wide-tease-item__info-wrapper > a', '.wide-tease-item__wrapper .wide-tease-item__headline'),
            ('[class^="styles_item__"] [class^="styles_teaseTitle__"] > a', '[class^="styles_item__"] [class^="styles_teaseTitle"]'),
            ('[class^="styles_item__"] [class^="styles_headline__"] > a', '[class^="styles_item__"] [class^="styles_headline"]'),
            ('[class^="tease-card"] [class^="tease-card__headline"]', '[class^="tease-card"] [class^="tease-card__headline"]'),
            ('[class^="related-content"] [class^="related-content"][class$="__headline"] > a', '[class^="related-content"] [class^="related-content"][class$="__headline"]'),
            ('[class^="storyline__headline"] > a', '[class^="storyline__headline"]'),
            ('[class^="styles_headline__"] > a', '[class^="styles_headline"]'),
        ]
        
        title_selector = ('h1',['article-hero-headline__htag'])
        date_selector = ('time',['relative'])
        date_format = '%B %d, %Y, %I:%M %p'
        image_selector = ('div',['article-hero__media-container', 'article-body__content'], 'src')
        content_selector = ('div',['article-body__content'])
        super().__init__(base_url, article_url_css_selector, title_selector, date_selector, date_format, image_selector, content_selector, urls_blacklist)
        
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
    
    def scrape_image(self, soup):
        #getting the image of the article
        image_url = None
        for image_class in self.image_selector[1]:
            image_tags = soup.find_all(self.image_selector[0], class_=image_class)
            for image_tag in image_tags:
                if image_tag and image_tag.find('img') and self.image_selector[2] in image_tag.find('img').attrs:
                    image_url = image_tag.find('img')[self.image_selector[2]]
                
                #check if image_url starts with http
                if image_url and not image_url.startswith('http'):
                    image_url = None
                
                if image_url and image_url.startswith('http'):
                    return image_url
        return image_url
