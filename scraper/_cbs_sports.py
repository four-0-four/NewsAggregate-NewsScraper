from scraper.news_scraper import NewsScraper

class CBSSportsNewsScraper(NewsScraper):
    def __init__(self, base_url, urls_blacklist):
        
        #(css_to_url, css_to_title)
        article_url_css_selector = [
            [('main.highlander-page-container a', f'main.highlander-page-container a h{i}') for i in range(1, 4)],
            [('div.container a', f'div.container h{i}') for i in [3, 5]],
            #('main.highlander-page-container a', 'main.highlander-page-container a h1'),
            #('main.highlander-page-container a', 'main.highlander-page-container a h2'),
            #('main.highlander-page-container a', 'main.highlander-page-container a h3'),
            #('div.container a', 'div.container h3'),
            #('div.container a', 'div.container h5'),   
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
    
    # Get the image
    def scrape_image(self, soup):
        figure_tag = soup.find('img', class_='Article-featuredImageImg is-lazy-image')
        if figure_tag:
            image_url = figure_tag['data-lazy']
            return image_url
        else:
            return None
