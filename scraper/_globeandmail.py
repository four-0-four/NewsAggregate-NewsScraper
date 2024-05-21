from datetime import datetime
from scraper.news_scraper import NewsScraper


class GlobeandMailScraper(NewsScraper):
    def __init__(self, base_url, urls_blacklist):
        
        #(css_to_url, css_to_title)
        article_url_css_selector = [
            ('div.LayoutTopPackageCard__StyledContainer-sc-11dx1zb-0 a', 'div.LayoutTopPackageCard__StyledContainer-sc-11dx1zb-0 p'), 
            ('div.Container__StyledContainer-sc-15gjlsr-0 a', 'div.Container__StyledContainer-sc-15gjlsr-0 a'),
            ('div.c-card a', 'div.c-card h3')
        ]
    
        title_selector = ('h1',['c-primary-title'])
        date_selector = ('time',['c-timestamp u-no-wrap text-gmr-5 font-gmsans'])
        date_format = '%Y-%m-%d %H:%M:%S'
        image_selector = ('div',['Image__StyledImageWrapper-sc-2118b8-0 YFlni c-image-wrapper l-media'])
        content_selector = ('article', 'default__StyledArticle-ivh5si-0 kggiAl l-article')
        super().__init__(base_url, article_url_css_selector, title_selector, date_selector, date_format, image_selector, content_selector, urls_blacklist)

    #Getting the titles
    def scrape_article_url_css(self):
        div_tag = self.article_url_css_selector[1][1]
        if div_tag:
            article_title = div_tag.get('data-sophi-label')
            if article_title:
                return article_title
            title_tag = div_tag.find('h3')
            title = title_tag.find('span') if title_tag else None
            return title
        return None

    # Getting the datetime
    def scrape_date(self, soup):
        datetime_value = soup.find('time')['datetime']
        
        # Convert str into datetime_obj
        datetime_object = datetime.strptime(datetime_value, '%Y-%m-%dT%H:%M:%S.%fZ')
        datetime_format = datetime_object.strftime('%Y-%m-%d %H:%M:%S')
        return datetime_format

    # Getting the image
    def scrape_image(self, soup):
        div_tag = soup.find(self.image_selector[0], class_=self.image_selector[1])
        if div_tag:
            img_tag = div_tag.find('img', class_='c-image')
            img_url = img_tag['src']
            return img_url
        else:
            None
            
    #get the content of the article
    def scrape_description(self, soup):
        content_tags = soup.find(self.content_selector[0], class_=self.content_selector[1])
        p_tags = content_tags.find_all('p')
        content = ""
        for p_tag in p_tags:
            p = p_tag.get_text(separator=' ', strip=True)
            content += p
                
        return content if content and len(content) >= 100 else None   
    

    