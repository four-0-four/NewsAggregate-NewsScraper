import pytest
from unittest.mock import patch, Mock
from scraper._globeandmail import GlobeandMailScraper
import json
from tests.test_helper import helper_test_article, helper_test_category_url_scraper, read_html_file, read_json_file
        
base_url = "https://www.theglobeandmail.com"
blacklist_url = []
       
# Expected result based on the sample HTML
expected_result = {
    "title": "CN Rail and CPKC workers vote to go on strike later this month if labour deal isn\u2019t reached",
    "date": "2024-05-01 17:55:36",
    "content": "Paul Boucher, President, Teamsters Canada Rail Conference speaks during a press conference to announce the results of strike votes at Canadian National and Canadian Pacific Kansas City on Parliament Hill in Ottawa on May 1. Sean Kilpatrick/The Canadian PressLog in or create a free account to listen to this article.Train operators at both of Canada\u2019s major freight railways have voted to go on strike later in May if a labour deal isn\u2019t reached, handing their union strong negotiating mandates and raising the odds of a work stoppage that would bring high economic costs.May 22 is the strike or lockout deadline for about 9,300 rail workers, who operate trains and direct traffic at Canadian National Railway Co. CNR-T +0.49% increase and Canadian Pacific Kansas City Ltd. CP-T +0.34% increase . The vote results announced on Wednesday give union leaders the right to call strikes with 72-hour notices.Paul Boucher, president of Teamsters Canada Rail Conference, said a combined 98 per cent of votes cast were in favour of a strike, with a participation rate of 93 per cent.The main issues for union bargaining teams are rest periods and the ability of employees to book time off to ensure they are not working while fatigued, Mr. Boucher said at a news conference in Ottawa on Wednesday. He accused the companies of trying to strip employees\u2019 rights to book rest periods to compensate for a labour shortage and retention problems.\u201cThe company\u2019s intentions are to squeeze more out of their employees because they can\u2019t find enough people,\u201d Mr. Boucher said. \u201cCompromising on safety is never the solution to staffing problems. CN and CPKC should instead be looking to improve working conditions and adopt a more humane approach to railroading.\u201dCPKC said in a press release its proposals do not compromise safety. Both railways say they have offered to move away from a pay-per-mile system to an hourly pay rate that offers more predictable days off.\u201cA work stoppage will impact all Canadians. It will halt freight traffic on CPKC\u2019s Canadian rail network. It would disrupt essential supply chains throughout North America, and significantly constrain trade between Canada and the U.S. and Mexico,\u201d CPKC said.In a statement, CN said it is negotiating to protect the supply chain and economy while offering employees a \u201cfair deal.\u201d\u201cThe union has made it clear that it will not agree to move toward a more modern agreement based on an hourly rate and scheduling that would have provided significant wage increases and offered scheduled consecutive days off, provisions for no layoffs, and reduced hours away from home,\u201d CN said.The workers are represented by three separate collective agreements at the two companies \u2013 two at Calgary-based CPKC and one at Montreal-based CN.It is not common for work stoppage deadlines to occur simultaneously at both freight haulers.The recent contracts expired at the end of 2023, and negotiators have been in talks since the fall.Teamsters represents about 130,000 workers in Canada.Some commuter rail services would also be halted because they are hosted or controlled by workers at the freight railways. These include Montreal\u2019s Exo, Toronto\u2019s Metrolinx and Vancouver\u2019s West Coast Express.Bob Ballantyne, a senior adviser to the Freight Management Association of Canada, said there are almost no real alternatives to railways for large retailers and commodity companies, which need to move large volumes of goods over long distancesA strike \u201cwould cause a lot of trouble for mining companies, forestry companies, the grain industry and chemical producers,\u201d Mr. Ballantyne said by phone.An informative summary of the day\u2019s top business headlines, features and columns.Register to sign up Explore newsletters",
    "image_url": "./globeandmail_article_files/7NABDL5QBNBMPHW3LY5IFKDDKI.jpg",
    "url": "http://theglobeandmail.com/test-article"
}
 
homepage_expected_result = read_json_file("tests/globeandmail/article_homepage_result.json")
category_1_expected_result = read_json_file("tests/globeandmail/article_category_1_result.json")
category_2_expected_result = read_json_file("tests/globeandmail/article_category_2_result.json")


# Test function using pytest
@pytest.mark.parametrize("article_url, expected", [
    ("http://theglobeandmail.com/test-article", expected_result)
])
def test_scrape_article(article_url, expected):
    scraper = GlobeandMailScraper(base_url=base_url, urls_blacklist=blacklist_url)
    path_html='tests/globeandmail/globeandmail_article.html'
    helper_test_article(scraper, article_url, expected, path_html)


# Test function using pytest
@pytest.mark.parametrize("category_path, expected", [
    ("/", homepage_expected_result)  # Ensure homepage_expected_result is defined
])
def test_fetch_article_urls_homepage(category_path, expected):
    scraper = GlobeandMailScraper(base_url=base_url, urls_blacklist=blacklist_url)
    path_html = 'tests/globeandmail/globeandmail_homepage.html'
    helper_test_category_url_scraper(scraper, category_path, expected, path_html)

      
# Test function using pytest
@pytest.mark.parametrize("category_path, expected", [
    ("/category1", category_1_expected_result)  # Ensure homepage_expected_result is defined
])
def test_fetch_article_urls_category_1(category_path, expected):
    scraper = GlobeandMailScraper(base_url=base_url, urls_blacklist=blacklist_url)
    path_html = 'tests/globeandmail/globeandmail_category_1.html'
    helper_test_category_url_scraper(scraper, category_path, expected, path_html)


# Test function using pytest
@pytest.mark.parametrize("category_path, expected", [
    ("/category2", category_2_expected_result)  # Ensure homepage_expected_result is defined
])
def test_fetch_article_urls_category_2(category_path, expected):
    scraper = GlobeandMailScraper(base_url=base_url, urls_blacklist=blacklist_url)
    path_html = 'tests/globeandmail/globeandmail_category_2.html'
    helper_test_category_url_scraper(scraper, category_path, expected, path_html)

