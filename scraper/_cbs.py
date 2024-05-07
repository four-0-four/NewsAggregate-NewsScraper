from scraper.news_scraper import NewsScraper

class CBSNewsScraper(NewsScraper):
    def __init__(self, base_url, urls_blacklist):
        
        #(css_to_url, css_to_title)
        article_url_css_selector = [
            ('article.item a', 'article.item a h4'), 
            ('ul.item__related-links', 'ul.item__related-links'),
            ('article.content content-article lazyloaded a', 'article.content content-article lazyloaded a > h1'),
            ('div.item a', 'div.item__title-wrapper.item__hed'),
        ]
        
        title_selector = ('h1',['content__title'])
        date_selector = ('time',['relative'])
        date_format = '%B %d, %Y, %I:%M %p'
        image_selector = ('div',['poster'], 'src')
        content_selector = ('section',['content__body'])
        super().__init__(base_url, article_url_css_selector, title_selector, date_selector, date_format, image_selector, content_selector, urls_blacklist)

