from datetime import datetime, timezone
import pytest
from unittest.mock import patch, Mock
from scraper._cbs import CBSNewsScraper
import json
from tests.test_helper import helper_test_article, helper_test_category_url_scraper, read_html_file, read_json_file
        
base_url = "https://www.cbsnews.com"
blacklist_url = []
       
# Expected result based on the sample HTML
expected_result = {
    "title": "Missouri man who crashed U-Haul into White House security barrier pleads guilty",
    "date": datetime(2024, 5, 13, 20, 39, 44, tzinfo=timezone.utc),
    "content": "A Missouri man has pleaded guilty to crashing a U-Haul into a White House security barrier in May 2023. Sai Kandula, 20, wearing an orange jail jumpsuit and speaking softly from the podium of a Washington, D.C., federal courtroom, acknowledged he had deliberately slammed into a security bollard in a failed attempt to seize power at the White House and install a dictatorship aligned with Nazi beliefs.Kandula pleaded guilty to a federal charge of willful depredation of federal property and will face a recommended 8 years in prison when he's sentenced on Aug. 23. CBS News was present during Kandula's plea agreement hearing Monday, during which prosecutors and the judge referenced a possible terrorism enhancement at Kandula's sentencing. The charge has a 10-year maximum prison term and a maximum $250,000 fine.The crime occurred at 16th and H Streets, Northwest, outside the White House last May.\u00a0 Kandula had a Nazi flag with him when he was arrested, according to court documents. According to the government's statement of facts, he said his goal was to \"get to the White House, seize power, and be put in charge of the nation.\"According to the statement of facts, \"When agents asked how Kandula would seize power, he stated he would 'Kill the President if that's what I have to do and would hurt anyone that would stand in my way.'\" He told investigators he had been \"planning for six months.\"During court proceedings Monday, Kandula said he had recently begun taking medication for schizophrenia while he's been incarcerated in pretrial detention. A psychiatric witness is expected to speak about Kandula's health during the August sentencing hearing, according to a defense attorney.The Justice Department said the damage incurred at the White House was approximately $4,322 as a result of Kandula's crashing of the U-Haul into the barrier.Scott MacFarlane is a congressional correspondent. He has covered Washington for two decades, earning 20 Emmy and Edward R. Murrow awards. His reporting has resulted directly in the passage of five new laws.",
    "image_url": "https://assets2.cbsnewsstatic.com/hub/i/r/2023/05/24/46b1c6f0-eb88-4d08-a2e2-970a8cac0a39/thumbnail/1280x720/42ceea5abeb0b7f605f74b1ce6b334b7/0524-en-truck-1996086-640x360.jpg?v=da1edae61593776e0985328155219700",
    "url": "http://cbsnews.com/test-article"
}
 
homepage_expected_result = read_json_file("tests/cbs/article_homepage_result.json")
category_1_expected_result = read_json_file("tests/cbs/article_category_1_result.json")
category_2_expected_result = read_json_file("tests/cbs/article_category_2_result.json")


# Test function using pytest
@pytest.mark.parametrize("article_url, expected", [
    ("http://cbsnews.com/test-article", expected_result)
])
def test_scrape_article(article_url, expected):
    scraper = CBSNewsScraper(base_url=base_url, urls_blacklist=blacklist_url)
    path_html='tests/cbs/cbs_article.html'
    helper_test_article(scraper, article_url, expected, path_html)


# Test function using pytest
@pytest.mark.parametrize("category_path, expected", [
    ("/", homepage_expected_result)  # Ensure homepage_expected_result is defined
])
def test_fetch_article_urls_homepage(category_path, expected):
    scraper = CBSNewsScraper(base_url=base_url, urls_blacklist=blacklist_url)
    path_html = 'tests/cbs/cbs_homepage.html'
    helper_test_category_url_scraper(scraper, category_path, expected, path_html)
        
        
# Test function using pytest
@pytest.mark.parametrize("category_path, expected", [
    ("/category1", category_1_expected_result)  # Ensure homepage_expected_result is defined
])
def test_fetch_article_urls_category_1(category_path, expected):
    scraper = CBSNewsScraper(base_url=base_url, urls_blacklist=blacklist_url)
    path_html = 'tests/cbs/cbs_category_1.html'
    helper_test_category_url_scraper(scraper, category_path, expected, path_html)


# Test function using pytest
@pytest.mark.parametrize("category_path, expected", [
    ("/category2", category_2_expected_result)  # Ensure homepage_expected_result is defined
])
def test_fetch_article_urls_category_2(category_path, expected):
    scraper = CBSNewsScraper(base_url=base_url, urls_blacklist=blacklist_url)
    path_html = 'tests/cbs/cbs_category_2.html'
    helper_test_category_url_scraper(scraper, category_path, expected, path_html)

