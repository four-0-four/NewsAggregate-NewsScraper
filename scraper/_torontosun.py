from datetime import datetime
from scraper.news_scraper import NewsScraper
import pytz

class TorontoSunScraper(NewsScraper):
    def __init__(self, base_url, urls_blacklist):
        
        #(css_to_url, css_to_title)
        article_url_css_selector = [
            ('a.article-card__link', 'a.article-card__link'), 
            ('a.item-label-href', 'a.item-label-href'),
        ]
        
        title_selector = ('h1',['article-title'])
        date_selector = ('',[''])
        date_format = ''
        image_selector = ('img',['featured-image__image'], 'src')
        content_selector = ('section',['article-content__content-group'])
        super().__init__(base_url, article_url_css_selector, title_selector, date_selector, date_format, image_selector, content_selector, urls_blacklist)
    
    #Getting the titles
    def scrape_article_url_css(self):
        for self.article_url_css_selector in range[0],[1]:
            div_tag = self.article_url_css_selector[1]
            if div_tag:
                article_title = div_tag.get('aria-label')
                if article_title:
                    return article_title
                title_tag = div_tag.get('title')
                return title_tag
            return None
    
    #get the content of the article
    def scrape_description(self, soup):
        content_class = 'article-content__content-group'
        for content_class in self.content_selector[1]:
            content_tags = soup.select(self.content_selector[0], class_=content_class)
            content = ""
            for content_tag in content_tags:
                p_tags = content_tag.find_all('p')
                for p_tag in p_tags:
                    p = p_tag.get_text(separator=' ', strip=True)
                    content += p

        return content if content and len(content) >= 100 else None
          
