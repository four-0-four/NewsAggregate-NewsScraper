from datetime import datetime
import json
import importlib
from concurrent.futures import ThreadPoolExecutor

def load_scraper(config):
    module_name = f"scraper.{config['module']}"
    class_name = config["class"]
    module = importlib.import_module(module_name)
    scraper_class = getattr(module, class_name)
    return scraper_class(config["base_url"])


def datetime_converter(o):
    if isinstance(o, datetime):
        return o.__str__()


def main():
    with open('config.json') as file:
        config = json.load(file)
        articles_categorized = {}
        article_urls_categorized = {} #the keys are category paths
        for source, details in config.items():
            print("getting the news ________________ " + source)
            scraper = load_scraper(details)
            article_urls_categorized = scraper.fetch_article_urls_all_categories(details["category_path"])
            
            for category, article_urls in article_urls_categorized.items():
                articles_categorized[category] = []
                for article_url in article_urls:
                    article_data = scraper.scrape_article(article_url)
                    articles_categorized[category].append(article_data)
                print(f"{category}: {len(articles_categorized[category])}")
            
            # Writing articles to a json file
            with open('articles.json', 'w') as outfile:
                json.dump(articles_categorized, outfile, indent=4, default=datetime_converter)

def scrape_one():
    article_url = 'https://abcnews.go.com/Entertainment/wireStory/sin-city-city-angels-building-starts-high-speed-109484497'
    with open('config.json') as file:
        config = json.load(file)
        scraper = load_scraper(config["ABCNews"])
        article_data = scraper.scrape_article(article_url)
        print(article_data)

if __name__ == '__main__':
    main()
