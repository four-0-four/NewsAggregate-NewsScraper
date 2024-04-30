from scraper.news_scraper import NewsScraper

class ABCNewsScraper(NewsScraper):
    def __init__(self, base_url, urls_blacklist):
        
        #(css_to_url, css_to_title)
        article_url_css_selector = [
            ('.ContentRoll__Item', '.ContentRoll__Item > h2'), 
            ('.ContentList__Item', '.ContentList__Item > h2'), 
            ('.AnchorLink.News', 'a.AnchorLink.News'),
            ('.CarouselSlide', '.CarouselSlide > h3'),
            ('.block', '.block > h4, .block > .content > a'),
            ('.band__common', '.band__common > a'),
            ('[class^="LatestHeadlines__item"] > a', '[class^="LatestHeadlines__item"] > h4')
        ]
        
        title_selector = ('h1',['vMjAx UdOCY WaKtx eHrJ mTgUP WimTs'])
        date_selector = ('div',['VZTD mLASH'])
        date_format = '%B %d, %Y, %I:%M %p'
        image_selector = ('div',['MediaPlaceholder', 'InlineImage GpQCA lZur asrEW'], 'src')
        content_selector = ('div',['xvlfx ZRifP TKoO eaKKC bOdfO'])
        super().__init__(base_url, article_url_css_selector, title_selector, date_selector, date_format, image_selector, content_selector, urls_blacklist)
        
    def scrape_title(self, soup):
        # Locate the <div> with the specified data-testid attribute
        div_tag = soup.find('div', attrs={'data-testid': 'prism-headline'})
        if div_tag:
            # Find the <h1> tag within this <div>
            h1_tag = div_tag.find('h1')
            if h1_tag:
                # Extract text from the <h1> tag
                title = h1_tag.get_text(separator=' ', strip=True)
                return title
        return None
    
    def scrape_description(self, soup):
        #getting the content of the article
        for content_class in self.content_selector[1]:
            content_tag = soup.find(self.content_selector[0], class_=content_class)
            if(content_tag):
                content = content_tag.get_text(separator=' ', strip=True)
            
                #check the content has certain length
                if content and len(content) < 100:
                    return None
                
                return content
            
        return None
