import requests
from bs4 import BeautifulSoup
from datetime import datetime

class NewsScraper:
    def __init__(self, base_url, article_url_css_selector, title_selector, date_selector, date_format, image_selector, content_selector):
        self.base_url = base_url
        self.article_url_css_selector = article_url_css_selector
        self.title_selector = title_selector
        self.date_selector = date_selector
        self.date_format = date_format
        self.image_selector = image_selector
        self.content_selector = content_selector

    def fetch_article_urls_all_categories(self, category_list):
        urls_all_categories = {}
        for category, category_id in category_list.items():
            urls_one_category = self.fetch_article_urls_one_category(category)
            urls_all_categories[category] = urls_one_category
        return urls_all_categories

    def fetch_article_urls_one_category(self, category_path):
        url = f"{self.base_url}{category_path}"
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        elements = soup.select(self.article_url_css_selector)
        article_links = []
        for element in elements:
            link_tag = element.find('a')  # find <a> tags within the selected elements
            if link_tag and 'href' in link_tag.attrs:
                href = link_tag['href']
                # Ensure the link is absolute
                if(href.startswith('http')):
                    full_link = href
                else:
                    continue
                article_links.append(full_link)

        return article_links

    def scrape_article(self, article_url):
        response = requests.get(article_url)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        title = self.scrape_title(soup)
        #print("Title:", title)
        date = self.scrape_date(soup)
        #print("Date:", date)
        content = self.scrape_description(soup)
        #print("Content:", content)
        
        if not title or not date or not content:
            return None
        
        image_url = self.scrape_image(soup)

        return {"title": title, "date": date, "content": content, "image_url": image_url}

    def scrape_title(self, soup):
        #getting the title of the article
        for title_class in self.title_selector[1]:
            h1_tag = soup.find(self.title_selector[0], class_=title_class)
            if(h1_tag):
                title = h1_tag.get_text(separator=' ', strip=True)
                return title
        return None
    
    def scrape_date(self, soup):
        #getting the date of the article
        for date_class in self.date_selector[1]:
            date_tag = soup.find(self.date_selector[0], class_=date_class)
            if(date_tag):
                date = date_tag.get_text(separator=' ', strip=True)
            
                try:
                    date_object = datetime.strptime(date, self.date_format)
                    return date_object
                except ValueError as e:
                    print("There was an error converting the date:", e)
                    return None
        
        return None
    
    def scrape_image(self, soup):
        #getting the image of the article
        image_url = None
        for image_class in self.image_selector[1]:
            image_tag = soup.find(self.image_selector[0], class_=image_class)
            if image_tag and image_tag.find('img') and self.image_selector[2] in image_tag.find('img').attrs:
                image_url = image_tag.find('img')[self.image_selector[2]]
            
            #check if image_url starts with http
            if image_url and not image_url.startswith('http'):
                image_url = None
            
            if image_url and image_url.startswith('http'):
                return image_url
        return image_url
    
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
