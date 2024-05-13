from datetime import datetime
import pytest
from unittest.mock import patch, Mock
from scraper._cbs import CBSNewsScraper
import json

from tests.test_helper import helper_test_article, helper_test_category_url_scraper, read_html_file, read_json_file
        
base_url = "https://cbsnews.com"
blacklist_url = []
        
# Expected result based on the sample HTML
expected_result = {
    "title": "Spectacular photos show the northern lights around the world",
    "date": "2024-05-12 15:09:31+00:00",
    "content": "A series of powerful solar storms colored skies across the Northern Hemisphere this weekend, as people witnessed brilliant displays of the northern lights in the United States, Canada, Europe, China and beyond. Officials have said the dazzling light shows could continue for several more days.The aurora borealis \u2014 the phenomenon more commonly known as the northern lights \u2014 happens because of a molecular collision in the upper levels of Earth's atmosphere that causes bursts of energy to be released in the form of visible light. The aurora borealis has a counterpart, the aurora australis, or southern lights, which is the same phenomenon in the southern hemisphere. These light shows can be visible for as much as half the year in certain places near either of the planet's two poles, but it's uncommon to see them in areas that are closer to the equator, which is why the spectacles over North America , Europe and other places on similar latitutdes were such a treat in the last few days.The aurora will extend from the poles toward the equator in periods of intense space weather activity, and it has been known in the past to reach as far as the continental U.S. when the activity is particularly extreme. That was the case over the weekend, as an unusually strong geomagnetic storm reached Earth and set the stage for a string of explosive nighttime scenes world over. The geomagnetic storm that arrived on Friday was a historic G5 , the highest level on a ranking scale that starts at G1, according to the National Oceanic and Atmospheric Administration.Additional Aurora sightings (weather permitting) may be possible this evening into tomorrow! A Geomagnetic Storm Watch has been issued for Sunday, May 12th.  Periods of G4-G5 geomagnetic storms are likely! \ud83d\udc40 https://t.co/iibFBuyzXoA solar storm of that size has not come into contact with Earth in decades. It arrived in the midst of a parade of coronal mass ejections \u2014 eruptions of magnetic field and other solar material from the Sun's corona that can cause geomagnetic storms \u2014 which continued to fuel the northern lights shows throughout Friday and Saturday. The next bursts of solar material are expected to arrive at Earth midday on Sunday , according to NOAA's Space Weather Prediction Center, which issued a geomagnetic storm watch in anticipation of G4 or G5 events likely following those upcoming coronal mass ejections.\"Watches at this level are very rare,\" the space weather prediction center said in an advisory on Saturday. It noted that the oncoming solar activity could potentially cause the aurora to \"become visible over much of the northern half of the country, and maybe as far south as Alabama to northern California.\"Ahead of the next round of solar flares, here's a look at some brilliant auroras that have materialized so far this weekend in different parts of the world.Emily Mae Czachor is a reporter and news editor at CBSNews.com. She covers breaking news, often focusing on crime and extreme weather. Emily Mae has previously written for outlets including the Los Angeles Times, BuzzFeed and Newsweek.",
    "image_url": "https://assets1.cbsnewsstatic.com/hub/i/r/2024/05/11/1e48a5f4-46da-4634-b831-1f8c2735b45d/thumbnail/1280x720/1611d278287703089eadd07d1abd29e8/george.jpg?v=218688c1357f974b9630d4fa8914721c",
    "url": "http://cbsnews.com/test-article"
}


#homepage_expected_result = read_json_file("tests/cbs/article_homepage_result.json")
#category_1_expected_result = read_json_file("tests/cbs/article_category_1_result.json")
#category_2_expected_result = read_json_file("tests/cbs/article_category_2_result.json")

# Test function using pytest
@pytest.mark.parametrize("article_url, expected", [
    ("http://cbsnews.com/test-article", expected_result)
])
def test_scrape_article(article_url, expected):
    scraper = CBSNewsScraper(base_url=base_url, urls_blacklist=blacklist_url)
    path_html='tests/cbs/cbs_article.html'
    helper_test_article(scraper, article_url, expected, path_html)
    
'''       
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

''' 