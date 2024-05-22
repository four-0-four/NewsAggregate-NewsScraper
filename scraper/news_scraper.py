import requests
from bs4 import BeautifulSoup
from datetime import datetime

class NewsScraper:
    def __init__(self, base_url, article_url_css_selector, title_selector, date_selector, date_format, image_selector, content_selector, urls_blacklist):
        self.base_url = base_url
        self.article_url_css_selector = article_url_css_selector
        self.title_selector = title_selector
        self.date_selector = date_selector
        self.date_format = date_format
        self.image_selector = image_selector
        self.content_selector = content_selector
        
        self.urls_blacklist = urls_blacklist
        self.added_urls = []
        self.article_links = []

    def read_html_file(self, file_path):
        with open(file_path, 'r', encoding='utf-8') as file:
            return file.read()


    def check_article_url(self, href):
        # Ensure the link is absolute
        if(href.startswith(self.base_url)):
            full_link = href
        elif(href.startswith("/")):
            full_link = self.base_url + href
        else:
            return None
        
        
        is_url_blacklisted = False
        #check that the href not in urls_blacklist
        for url_blacklist in self.urls_blacklist:
            if url_blacklist in full_link:
                is_url_blacklisted = True
                break
        
        if is_url_blacklisted:
            return None
        
        return full_link
    
    def check_if_article_is_duplicate(self, href, full_link, text):
        if (full_link in self.added_urls):
            # Check if the URL exists in article_links and has an empty title
            for article in self.article_links:
                if article['url'] == href and ( not article['title'] or len(article['title']) < len(text) ):
                    self.article_links.remove(article)  # Remove if title is empty
                    return False
            return True
        return False
    
    def fetch_article_urls_all_categories(self, category_list):
        urls_all_categories = {}
        for category, category_id in category_list.items():
            urls_one_category = self.fetch_article_urls_one_category(category)
            urls_all_categories[category] = urls_one_category
        return urls_all_categories

    def fetch_article_urls_one_category(self, category_path):
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'
        }
        url = f"{self.base_url}{category_path}"
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.text, 'html.parser')
        #custom_html = self.read_html_file("tests/cnn/cnn_category_1.html")
        #soup = BeautifulSoup(custom_html, 'html.parser')
        
        self.article_links = []
        #print(len(self.article_url_css_selector))
        for potential_article in self.article_url_css_selector:
            article_info = {"title":"", "url":""}
            elements = soup.select(potential_article[0])
            #print("****************************")
            #print(potential_article[0])
            for element in elements:
                if element.name == 'a':
                    link_tags = [element]
                else:
                    link_tags = element.find_all('a')  # find <a> tags within the selected elements
                
                for link_tag in link_tags:
                    if link_tag and 'href' in link_tag.attrs:
                        href = link_tag['href']
                        #print(href)
                        full_link = self.check_article_url(href)
                        if not full_link:
                            continue
                        
                        #get text
                        title_tag = element.select_one(potential_article[1])
                        text = title_tag.get_text(strip=True) if title_tag else link_tag.get_text(strip=True)
                        
                        
                        #check that we have already added it so we don't add twice
                        if self.check_if_article_is_duplicate(href, full_link, text):
                            continue
                        
                        
                        self.added_urls.append(full_link)
                        article_info = {"title": text, "url": full_link, "title select": potential_article[1], "link select": potential_article[0]}
                        self.article_links.append(article_info)

        return self.article_links

    def scrape_article(self, article_url):
        print(article_url)
        response = requests.get(article_url)
        soup = BeautifulSoup(response.text, 'html.parser')
        #custom_html = self.read_html_file("tests/cnn/cnn_article.html")
        #soup = BeautifulSoup(custom_html, 'html.parser')
        
        title = self.scrape_title(soup)
        print("Title:", title)
        date = self.scrape_date(soup)
        #print("Date:", date)
        content = self.scrape_description(soup)
        print("Content:", content)
        
        if not title or not date or not content or len(content) < 100:
            return None
        
        image_url = self.scrape_image(soup)
        print("Image:", image_url)

        return {"title": title, "date": date, "content": content, "image_url": image_url, "url": article_url}

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
                    #print("date: ", date)
                    date_object = datetime.strptime(date, self.date_format)
                    return date_object
                except ValueError as e:
                    #print("There was an error converting the date:", e)
                    return None
        
        return None
    
    def scrape_image(self, soup):
        #getting the image of the article
        image_url = 'https://torontosun.com/opinion/have-your-say-answer-our-daily-toronto-sun-poll-question-2'
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
