from scraper.news_scraper import NewsScraper

class SKYNewsScraper(NewsScraper):
    def __init__(self, base_url, urls_blacklist):
        
        #(css_to_url, css_to_title)
        article_url_css_selector = [
            
        ]
        
        title_selector = ('h1',['vMjAx UdOCY WaKtx eHrJ mTgUP WimTs'])
        #date_selector = ('div',['VZTD mLASH'])
        date_selector = ('div',['sina'])
        date_format = '%B %d, %Y, %I:%M %p'
        image_selector = ('div',['MediaPlaceholder', 'InlineImage GpQCA lZur asrEW'], 'src')
        content_selector = ('div',['xvlfx ZRifP TKoO eaKKC bOdfO'])
        super().__init__(base_url, article_url_css_selector, title_selector, date_selector, date_format, image_selector, content_selector, urls_blacklist)
        
