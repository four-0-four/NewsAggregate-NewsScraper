from datetime import datetime
import pytest
from unittest.mock import patch, Mock
from scraper._abc import ABCNewsScraper
import json

from tests.test_helper import helper_test_article, helper_test_category_url_scraper, read_html_file, read_json_file
        
base_url = "https://abcnews.go.com"
blacklist_url = []
        
# Expected result based on the sample HTML
expected_result = {
    "title": "Russian journalist detained for posts criticizing the military, his lawyer says", 
    "date": datetime(2024, 4, 26, 8, 15), 
    "content": "TALLINN, Estonia -- A journalist for the Russian edition of Forbes magazine has been detained on charges of spreading false information about the Russian military, his lawyer said Friday. Sergei Mingazov is being held in the Far Eastern city of Khabarovsk, lawyer Konstantin Bubon said on Facebook . He said that Mingazov was detained because of social media posts he made about the Ukrainian city of Bucha, where more than 400 bodies of civilians were found, many bearing signs of torture, after Russian forces pulled out in April 2022. Mingazov will appear in court on Saturday on the charge of spreading false information, which could send him to prison for 10 years if convicted. Russia cracked down severely on criticism of the war soon after launching a full-scale invasion of Ukraine in February 2022, passing laws that criminalize allegedly false information about the military or statements seen as discrediting the military. Related Stories Third man is detained in a major bribery case that involves Russia's deputy defense minister Apr 25, 4:38 AM A Russian actress who called for peace was fined for hosting an 'almost naked' party Apr 25, 7:45 AM A top Russian military official reportedly linked to Ukraine's Mariupol arrested for bribe-taking Apr 23, 5:06 PM Journalists, opposition figures and regular citizens have been swept up in the crackdown, many of them sentenced to long prison terms. The longest to be imposed was against prominent activist Vladimir Kara-Murza, who was sentenced to 25 years. ___ Follow the AP’s coverage of the war at https://apnews.com/hub/russia-ukraine", 
    "image_url": "https://i.abcnewsfe.com/a/fc17fa39-aa82-443b-ab16-e91d4d923d89/west_bank_human_rights_violations_reuters_nr_240426_hpMain_16x9.jpg?w=992", 
    "url": "http://fakeurl.com/test-article"
}

homepage_expected_result = read_json_file("tests/abc/article_homepage_result.json")
category_1_expected_result = read_json_file("tests/abc/article_category_1_result.json")
category_2_expected_result = read_json_file("tests/abc/article_category_2_result.json")

# Test function using pytest
@pytest.mark.parametrize("article_url, expected", [
    ("http://fakeurl.com/test-article", expected_result)
])
def test_scrape_article(article_url, expected):
    scraper = ABCNewsScraper(base_url=base_url, urls_blacklist=blacklist_url)
    path_html='tests/abc/abc_article.html'
    helper_test_article(scraper, article_url, expected, path_html)
    
        
# Test function using pytest
@pytest.mark.parametrize("category_path, expected", [
    ("/", homepage_expected_result)  # Ensure homepage_expected_result is defined
])
def test_fetch_article_urls_homepage(category_path, expected):
    scraper = ABCNewsScraper(base_url=base_url, urls_blacklist=blacklist_url)
    path_html = 'tests/abc/abc_homepage.html'
    helper_test_category_url_scraper(scraper, category_path, expected, path_html)
        

# Test function using pytest
@pytest.mark.parametrize("category_path, expected", [
    ("/category1", category_1_expected_result)  # Ensure homepage_expected_result is defined
])
def test_fetch_article_urls_category_1(category_path, expected):
    scraper = ABCNewsScraper(base_url=base_url, urls_blacklist=blacklist_url)
    path_html = 'tests/abc/abc_category_1.html'
    helper_test_category_url_scraper(scraper, category_path, expected, path_html)


# Test function using pytest
@pytest.mark.parametrize("category_path, expected", [
    ("/category2", category_2_expected_result)  # Ensure homepage_expected_result is defined
])
def test_fetch_article_urls_category_2(category_path, expected):
    scraper = ABCNewsScraper(base_url=base_url, urls_blacklist=blacklist_url)
    path_html = 'tests/abc/abc_category_2.html'
    helper_test_category_url_scraper(scraper, category_path, expected, path_html)

