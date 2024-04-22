
import requests
from bs4 import BeautifulSoup
from dateutil import parser
from datetime import datetime, timedelta

def fetch_articles(base_url, category_path, css_selector):
    """
    Fetch articles from a given category and return links to those articles.
    
    Parameters:
        base_url (str): The base URL of the news website.
        category_path (str): The path to the specific category of news.
        css_selector (str): CSS selector used to find the article links.
    """
    url = f"{base_url}{category_path}"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    # Find all elements using the provided CSS selector
    elements = soup.select(css_selector)

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


def scrape_article(article_url, TITLE_SELECTOR, DATE_SELECTOR, DATE_FORMAT, IMAGE_SELECTOR, CONTENT_SELECTOR):
    """
    Scrape the title and text of an article given its URL.
    """
    response = requests.get(article_url)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    print("about to scrape article")
    
    #getting the title of the article
    h1_tag = soup.find(TITLE_SELECTOR[0], class_=TITLE_SELECTOR[1])
    if(h1_tag):
        title = h1_tag.get_text(separator=' ', strip=True)
    else:
        return None
    
    print("Title:", title)
    
    #getting the date of the article
    date_tag = soup.find(DATE_SELECTOR[0], class_=DATE_SELECTOR[1])
    if(date_tag):
        date = date_tag.get_text(separator=' ', strip=True)
    else:
        return None
    
    print("Date:", date)
    
    try:
        date_object = datetime.strptime(date, DATE_FORMAT)
    except ValueError as e:
        print("There was an error converting the date:", e)
        return None
    
    #getting the content of the article
    content_tag = soup.find(CONTENT_SELECTOR[0], class_=CONTENT_SELECTOR[1])
    if(content_tag):
        content = content_tag.get_text(separator=' ', strip=True)
    else:
        return None
    print("Content:", content)
    #check the content has certain length
    if len(content) < 100:
        return None
    
    #getting the image of the article
    image_tag = soup.find(IMAGE_SELECTOR[0], class_=IMAGE_SELECTOR[1]).find('img')
    if image_tag and IMAGE_SELECTOR[2] in image_tag.attrs:
        image_url = image_tag[IMAGE_SELECTOR[2]]
    else:
        image_url = None
    print("Image URL:", image_url)
    #check if image_url starts with http
    if not image_url.startswith('http'):
        image_url = None

    return {"title": title, "date": date_object, "content": content, "image_url": image_url}

def main(base_url, categories, css_selector):
    """
    Main function to scrape a news site.
    """
    all_articles = []
    for category in categories:
        print(f"Scraping category: {category}")
        article_links = fetch_articles(base_url, category, css_selector)
        all_articles.extend(article_links)
    print(len(all_articles))




if __name__ == '__main__':
    # Create a new instance of the Scraper class
    #BASE_URL = 'https://abcnews.go.com'
    #CATEGORIES = ['/Health']
    #ARTICLE_CSS_SELECTOR = '.ContentRoll__Item, .ContentList__Item, .AnchorLink.News, .AnchorLink.News, .CarouselSlide, .block, .band__common'
    #main(BASE_URL, CATEGORIES, ARTICLE_CSS_SELECTOR)
    
    ARTICLE_URL = 'https://abcnews.go.com/US/usc-cancels-commencement-speakers-after-canceled-valedictorian-speech/story?id=109444698'
    
    TITLE_SELECTOR = ('h1',['vMjAx UdOCY WaKtx eHrJ mTgUP WimTs']) #list of classes to choose
    DATE_SELECTOR = ('div',['VZTD mLASH']) #list of classes to choose
    DATE_FORMAT = '%B %d, %Y, %I:%M %p'
    IMAGE_SELECTOR = ('div',['MediaPlaceholder', 'InlineImage GpQCA lZur asrEW'], 'src') #list of classes to choose
    CONTENT_SELECTOR = ('div',['xvlfx ZRifP TKoO eaKKC bOdfO']) #list of classes to choose
    
    article = scrape_article(ARTICLE_URL, TITLE_SELECTOR, DATE_SELECTOR, DATE_FORMAT, IMAGE_SELECTOR, CONTENT_SELECTOR)
    print(article)