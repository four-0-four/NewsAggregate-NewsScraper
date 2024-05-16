from datetime import datetime, timezone
import pytest
from unittest.mock import patch, Mock
from scraper._cbs_sports import CBSSportsNewsScraper
import json
from tests.test_helper import helper_test_article, helper_test_category_url_scraper, read_html_file, read_json_file
        
base_url = "https://www.cbssports.com"
blacklist_url = []
       
# Expected result based on the sample HTML
expected_result = {
    "title": "NFL schedule 2024: Complete list of games broadcast on CBS, including Eagles-Cowboys showdown in Week 10",
    "date": "2024-05-16 02:08:00 UTC",
    "content": "The NFL on CBS enters its 65th season broadcasting the league with plenty of exciting matchups. CBS Sports will have 10 national Sunday doubleheader windows in 2024, starting in Week 2 with the two-time defending champion Kansas City Chiefs hosting the Cincinnati Bengals in a showdown between the two teams who have represented the AFC in each of the past five Super Bowls. The Chiefs will be on CBS more than any other network in 2024, highlighting a massive part of the NFL on CBS schedule. Kansas City will be featured eight times on CBS, including a Week 2 showdown with the Bengals and a Week 11 matchup with the Buffalo Bills . The 4:25 p.m, EST national game window is highlighted by more highly-anticipated games on the CBS slate, including the Philadelphia Eagles at Baltimore Ravens (Week 13) and Buffalo Bills at Detroit Lions (Week 15). The Bills, Ravens, and Pittsburgh Steelers will also be on CBS a minimum of eight times this season. Three must-see NFC matchups highlight the slate , including the Philadelphia Eagles at Dallas Cowboys (Week 10) and Green Bay Packers at Los Angeles Rams (Week 5). The NFL ON CBS will finish the regular season strong with a national doubleheader in three of the final four weeks. Here is the complete 2024 NFL on CBS schedule Week 1 Sunday, September 8 Patriots at Bengals, 1 p.m. Texans at Colts , 1 p.m. Cardinals at Bills, 1 p.m. Jaguars at Dolphins , 1 p.m. Broncos at Seahawks , 1 p.m. Broncos at Seahawks, 4:05 p.m. Raiders at Chargers , 4:05 p.m. Week 2 Sunday, September 15 49ers at Vikings , 1 p.m. Raiders at Ravens, 1 p.m. Jets at Titans , 1 p.m. Browns at Jaguars, 1 p.m. Chargers at Panthers , 1 p.m. Bengals at Chiefs, 4:25 p.m. Steelers at Broncos, 4:25 p.m. Week 3 Sunday, September 22 Chargers at Steelers, 1 p.m. Texans at Vikings, 1 p.m. Bears at Colts, 1 p.m. Dolphins at Seahawks, 4:05 p.m. Panthers at Raiders, 4:05 p.m. Week 4 Sunday, September 29 Vikings at Packers, 1 p.m. Broncos at Jets, 1 p.m. Steelers at Colts, 1 p.m. Jaguars at Texans, 1 p.m. Chiefs at Chargers, 4:25 p.m. Browns at Raiders, 4:25 p.m. Week 5 Sunday, October 6 Bills at Texans, 1 p.m. Ravens at Bengals, 1 p.m. Colts at Jaguars, 1 p.m. Giants at Seahawks, 4:25 p.m. Packers at Rams, 4:25 p.m. Week 6 Sunday, October 13 Texans at Patriots, 1 p.m. Commanders at Ravens, 1 p.m. Colts at Titans, 1 p.m. Steelers at Raiders, 4:05 p.m. Chargers at Broncos, 4:05 p.m. Week 7 Sunday, October 20 Texans at Packers, 1 p.m. Bengals at Browns, 1 p.m. Titans at Bills, 1 p.m. Raiders at Rams, 4:05 p.m. Panthers at Commanders, 4:05 p.m. Week 8 Sunday, October 27 Ravens at Browns, 1 p.m. Jets at Patriots, 1 p.m. Colts at Texans, 1 p.m. Bears at Commanders, 1 p.m. Eagles at Bengals, 4:25 p.m. Chiefs at Raiders, 4:25 p.m. Panthers at Broncos, 4:25 p.m. Week 9 Sunday, November 3 Dolphins at Bills, 1 p.m. Colts at Vikings, 1 p.m. Broncos at Ravens, 1 p.m. Chargers at Browns, 1 p.m. Saints at Panthers, 1 p.m. Bears at Cardinals, 4:05 p.m. Week 10 Sunday, November 10 Broncos at Chiefs, 1 p.m. Steelers at Commanders, 1 p.m. Bills at Colts, 1 p.m. Eagles at Cowboys, 4:25 p.m. Jets at Cardinals, 4:25 p.m. Week 11 Sunday, November 17 Ravens at Steelers, 1 p.m. Raiders at Dolphins, 1 p.m. Vikings at Titans, 1 p.m. Jaguars at Lions, 1 p.m. Chiefs at Bills, 4:25 p.m. Bengals at Chargers, 4:25 p.m. Week 12 Sunday, November 24 Chiefs at Panthers, 1 p.m. Patriots at Dolphins, 1 p.m. Buccaneers at Giants, 1 p.m. Titans at Texans, 1 p.m. Broncos at Raiders, 4:05 p.m. Week 13 Thursday, November 28 (Thanksgiving Day) Bears at Lions, 12:30 p.m. Sunday, December 1 Chargers at Falcons , 1 p.m. Titans at Commanders, 1 p.m. Colts at Patriots, 1 p.m. Steelers at Bengals, 1 p.m. Eagles at Ravens, 4:25 p.m. Week 14 Sunday, December 8 Browns at Steelers, 1 p.m. Jets at Dolphins, 1 p.m. Raiders at Buccaneers, 1 p.m. Jaguars at Titans, 1 p.m. Seahawks at Cardinals, 4:05 p.m. Week 15 Sunday, December 15 Chiefs at Browns, 1 p.m. Dolphins at Texans, 1 p.m. Ravens at Giants, 1 p.m. Bills at Lions, 1 p.m. Colts at Browns, 4:25 p.m. Patriots at Cardinals, 4:25 p.m. Week 16 Sunday, December 22 Rams at Jets, 1 p.m. Patriots at Bills, 1 p.m. Titans at Colts, 1 p.m. 49ers at Dolphins, 4:25 p.m. Jaguars at Raiders, 4:25 p.m. Week 17 Sunday, December 29 Jets at Bills, 1 p.m. Titans at Jaguars, 1 p.m. Panthers at Buccaneers, 1 p.m. TBD, 4:05 p.m. Week 18 CBS Games TBD",
    "image_url": "https://sportshub.cbsistatic.com/i/r/2023/11/30/11147d05-edde-460d-a684-8251b6c3a750/thumbnail/770x433/08942a25b5152c58c01b7a61ba768c19/getty-jalen-hurts-dak-prescott.jpg",
    "url": "http://cbssports.com/test-article"
}
 
homepage_expected_result = read_json_file("tests/cbssports/article_homepage_result.json")
category_1_expected_result = read_json_file("tests/cbssports/article_category_1_result.json")
category_2_expected_result = read_json_file("tests/cbssports/article_category_2_result.json")


# Test function using pytest
@pytest.mark.parametrize("article_url, expected", [
    ("http://cbssports.com/test-article", expected_result)
])
def test_scrape_article(article_url, expected):
    scraper = CBSSportsNewsScraper(base_url=base_url, urls_blacklist=blacklist_url)
    path_html='tests/cbssports/cbssports_article.html'
    helper_test_article(scraper, article_url, expected, path_html)


# Test function using pytest
@pytest.mark.parametrize("category_path, expected", [
    ("/", homepage_expected_result)  # Ensure homepage_expected_result is defined
])
def test_fetch_article_urls_homepage(category_path, expected):
    scraper = CBSSportsNewsScraper(base_url=base_url, urls_blacklist=blacklist_url)
    path_html = 'tests/cbssports/cbssports_homepage.html'
    helper_test_category_url_scraper(scraper, category_path, expected, path_html)

        
# Test function using pytest
@pytest.mark.parametrize("category_path, expected", [
    ("/category1", category_1_expected_result)  # Ensure homepage_expected_result is defined
])
def test_fetch_article_urls_category_1(category_path, expected):
    scraper = CBSSportsNewsScraper(base_url=base_url, urls_blacklist=blacklist_url)
    path_html = 'tests/cbssports/cbssports_category_1.html'
    helper_test_category_url_scraper(scraper, category_path, expected, path_html)


# Test function using pytest
@pytest.mark.parametrize("category_path, expected", [
    ("/category2", category_2_expected_result)  # Ensure homepage_expected_result is defined
])
def test_fetch_article_urls_category_2(category_path, expected):
    scraper = CBSSportsNewsScraper(base_url=base_url, urls_blacklist=blacklist_url)
    path_html = 'tests/cbssports/cbssports_category_2.html'
    helper_test_category_url_scraper(scraper, category_path, expected, path_html)

