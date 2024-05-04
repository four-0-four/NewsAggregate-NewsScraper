from scraper.news_scraper import NewsScraper
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import time
import logging

class ESPNScraper(NewsScraper):
    def __init__(self, base_url, urls_blacklist):
        article_url_css_selector = [
            ('[data-id]', '[data-id]'),
        ]
        title_selector = ('h1', ['vMjAx UdOCY WaKtx eHrJ mTgUP WimTs'])
        date_selector = ('div', ['VZTD mLASH'])
        date_format = '%B %d, %Y, %I:%M %p'
        image_selector = ('div', ['MediaPlaceholder', 'InlineImage GpQCA lZur asrEW'], 'src')
        content_selector = ('div', ['xvlfx ZRifP TKoO eaKKC bOdfO'])
        super().__init__(base_url, article_url_css_selector, title_selector, date_selector, date_format, image_selector, content_selector, urls_blacklist)
        
        # Initialize Selenium WebDriver
        chrome_options = Options()
        chrome_options.add_argument("--headless")  # Run in background without opening a browser window
        chrome_options.add_experimental_option('excludeSwitches', ['enable-logging'])  # Suppress logging

        # Set the WebDriver log level to ignore less severe messages
        service = Service(ChromeDriverManager().install())
        service.log_path = 'NUL'  # Redirect logs to NUL to avoid console output on Windows
        self.driver = webdriver.Chrome(service=service, options=chrome_options)

    def fetch_article_urls_one_category(self, category_path):
        url = f"{self.base_url}{category_path}"
        self.driver.get(url)
        last_height = self.driver.execute_script("return document.body.scrollHeight")
        
        attempt = 0
        while attempt < 5:
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(3)
            new_height = self.driver.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                break
            last_height = new_height
            attempt += 1

        soup = BeautifulSoup(self.driver.page_source, 'html.parser')
        
        article_links = []
        for potential_article in self.article_url_css_selector:
            elements = soup.select(potential_article[0])
            for element in elements:
                link_tags = element.find_all('a') if element.name != 'a' else [element]
                for link_tag in link_tags:
                    if 'href' in link_tag.attrs:
                        href = link_tag['href']
                        full_link = href if href.startswith("http") else self.base_url + href
                        if any(blacklisted in full_link for blacklisted in self.urls_blacklist):
                            continue
                        if full_link not in self.added_urls:
                            self.added_urls.append(full_link)
                            title = link_tag.get_text(strip=True)
                            article_info = {"title": title, "url": full_link}
                            article_links.append(article_info)
        self.driver.quit()
        return article_links
