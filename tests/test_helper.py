from datetime import datetime
import pytest
from unittest.mock import patch, Mock
from scraper._cbs import CBSNewsScraper
import json


def datetime_converter(o):
    if isinstance(o, datetime):
        return o.__str__()

# Sample HTML that simulates an article page
def read_html_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return file.read()
    
def read_json_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return json.load(file)
    
def helper_test_article(scraper, article_url, expected, path_html):
    sample_html = read_html_file(path_html)

    # Mock requests.get to return a mock response with the sample HTML
    with patch('requests.get') as mocked_get:
        mock_response = Mock()
        mock_response.text = sample_html
        mocked_get.return_value = mock_response
        
        # Run the scrape_article method
        result = scraper.scrape_article(article_url)
        with open('articles_article_test.json', 'w') as outfile:
                json.dump(result, outfile, indent=4, default=datetime_converter)
        
        # Assert to check if the actual result matches the expected result
        assert result == expected, f"Expected {expected}, but got {result}"
        
        
def helper_test_category_url_scraper(scraper, category_path, expected, path_html):
    sample_html = read_html_file(path_html)

    # Mock requests.get to return a mock response with the sample HTML
    with patch('requests.get') as mocked_get:
        mock_response = Mock()
        mock_response.text = sample_html
        mocked_get.return_value = mock_response
        
        # Run the scrape_article method
        result = scraper.fetch_article_urls_one_category(category_path)
        category_path = category_path.replace("/","")
        with open(f'articles_cnn.json', 'w') as outfile:
                json.dump(result, outfile, indent=4, default=datetime_converter)
        
        # Assert to check if the actual result matches the expected result
        assert result == expected, f"Expected {expected}, but got {result}"
