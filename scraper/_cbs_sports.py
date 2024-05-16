from datetime import datetime
from scraper.news_scraper import NewsScraper
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

class CBSSportsNewsScraper(NewsScraper):
    def __init__(self, base_url, urls_blacklist):
        
        #(css_to_url, css_to_title)
        article_url_css_selector = [
            ('main.highlander-page-container a', 'main.highlander-page-container a h3'), #h1, h2
            ('div.container a', 'div.container h3'),
            ('div.container a', 'div.container h5'),
        ]
        
        title_selector = ('h1',['Article-headline'])
        date_selector = ('time',['TimeStamp'])
        date_format = '%Y-%m-%d %H:%M:%S %Z'
        image_selector = ('img',['Article-featuredImageImg is-lazy-image'], 'src')
        content_selector = ('div',['Article-bodyContent'])
        super().__init__(base_url, article_url_css_selector, title_selector, date_selector, date_format, image_selector, content_selector, urls_blacklist)
    
    # Get the datetime from time attribute
    def scrape_date(self, soup):
        datetime_value = soup.find('time')['datetime']
        return datetime_value

    def scrape_image(self, soup):
        figure_tag = soup.find('img', class_='Article-featuredImageImg is-lazy-image')
        if figure_tag:
            image_url = figure_tag['data-lazy']
            return image_url
        else:
            return None
