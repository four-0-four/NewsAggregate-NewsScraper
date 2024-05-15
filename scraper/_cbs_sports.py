from datetime import datetime
from scraper.news_scraper import NewsScraper
import pytz

class CBSSportsNewsScraper(NewsScraper):
    def __init__(self, base_url, urls_blacklist):
        
        #(css_to_url, css_to_title)
        article_url_css_selector = [
            ('main.highlander-page-container a', 'main.highlander-page-container a h3'), #h1, h2
            ('div.container a', 'div.container h3'),
            #('div.article-list-content-blocks-wrap a', 'div.article-list-content-blocks-wrap a h3'),
            #('section.article-list-single-lead a', 'section.article-list-single-lead h3'),
        ]
        
        title_selector = ('h1',['Article-headline'])
        date_selector = ('time',['TimeStamp'])
        date_format = '%Y-%m-%d %H:%M:%S %Z'
        image_selector = ('figure',['img'], 'data-lazy')
        #homepage_image = ('div',['article-list-item-image'], 'href')
        #homepage_image = ('div',['background-image'], ***style***)
        content_selector = ('div',['Article-bodyContent'])
        super().__init__(base_url, article_url_css_selector, title_selector, date_selector, date_format, image_selector, content_selector, urls_blacklist)
    
    # Get the datetime from time attribute
    def scrape_date(self, soup):
        datetime_value = soup.find('time')['datetime']
        return datetime_value
    
        # Convert str into datetime_obj
        #datetime_object = datetime.strptime(datetime_value, "%Y-%m-%dT%H:%M:%S%z")

    
    # Get the image
    def scrape_image(self, soup):
        figure_tag = soup.find(self.image_selector[0], class_=self.image_selector[1])
        if figure_tag:
            image_url = figure_tag['data_lazy']
            return image_url   

        else:
            print("No images found.")
            return None
    
    #get the content of the article
    def scrape_description(self, soup):
        div_content = soup.find('div', attrs={'class': 'Article-bodyContent'})
        if div_content:
            p_tags = div_content.find_all('p','h2')
            content = ""
            for p_tag in p_tags:
                p = p_tag.get_text(separator=' ', strip=True)
                content += p
                
        return content if content and len(content) >= 100 else None          