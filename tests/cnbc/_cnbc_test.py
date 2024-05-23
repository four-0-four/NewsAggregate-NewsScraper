import pytest
from unittest.mock import patch, Mock
from scraper._cnbc import CNBCNewsScraper
from datetime import datetime, timezone
import json

from tests.test_helper import helper_test_article, helper_test_category_url_scraper, read_html_file, read_json_file
        
base_url = "https://www.cnbc.com"
blacklist_url = []
        
# Expected result based on the sample HTML
expected_result = {
    "title": "China and India still rely heavily on coal, climate targets remain 'very difficult' to achieve",
    "date": datetime(2024, 5, 14, 0, 24, 12, tzinfo=timezone.utc),
    "content": " While India and China have ambitious plans to cut emissions, heavy reliance on coal \u2014 the dirtiest fossil fuel \u2014 continues to be the most reliable and affordable way of meet rising electricity demand. Global electricity generation from coal has been consistently rising for the last two decades, with the highest increases coming from China (+319 TWh) and India (+100 TWh) last year, according to a study by energy think tank Ember. China and India have not reduced coal generation for electricity, according to a new study, making it harder for Asia's largest carbon emitters to reach their climate targets. While both Asian countries have ambitious plans to cut emissions, heavy reliance on coal \u2014 the dirtiest fossil fuel \u2014 continues to be the most reliable and affordable way of meet rising electricity demand. Global electricity generation from coal has been consistently rising for the last two decades, nearly doubling from 5,809 terawatt-hours in 2000 to 10,434 TWh in 2023, a new study by energy think tank Ember found. The highest increases came from China (+319 TWh) and India (+100 TWh), the study showed. According to the IEA, coal remains the biggest energy source for electricity generation, supplying more than one-third of global\u00a0electricity. It will continue to play a crucial role in industries such as iron and steel until new technologies are available. \"It will be very difficult to meet targets without a rapid face down in coal. It'll certainly be out of reach,\" said Francis Johnson, senior research fellow and climate lead at the Stockholm Environment Institute's Asia Center. \"We're not phasing out coal fast enough,\" he warned. Asia's largest economy has two big climate goals: to strive fo r\u00a0peak carbon emissions in 2030, and reach carbon neutrality in 2060 . Still, reliance on coal has shown no signs of waning. Electricity demand in the East Asian nation has increased by sevenfold since the beginning of the decade, while coal demand has climbed by more than five times over the same period, Ember's research showed. China, the world's largest coal producer, emitted 5,491 million tonnes of carbon dioxide from electricity generation in 2023. That's at least three times more than the U.S. (1,570 MtCO2) and India (1,470 MtCO2), data from the study showed. However, the country has made notable progress in renewable energy development, leading to a slowdown in the rate of emission increase from an average of 9% annually between 2001 and 2015, to 4.4% annually between 2016 and 2023, the energy think tank said. \"China is very close to peak emissions and the clean energy transition is going extraordinarily fast,\" Dave Jones, global insights program director at Ember, told CNBC. \"Even with very high levels of electricity demand growth, it looks like the levels of renewables growth would be enough,\" Jones said. Clean electricity contributed to 35% of China's total electricity generation, the Ember report showed. Hydropower \u2014\u00a0 its second-largest energy source \u2014 made up 13% of that mix, while wind and solar combined reached new highs of 16% in 2023. \"Had wind and solar generation not increased since 2015, and demand had instead been met by coal, emissions would have been 20% higher in 2023,\" the report highlighted, adding that those two sources can now generate enough electricity to power Japan. But Stockholm Environment Institute's Johnson warned China still needs to be less dependent on other forms of fossil fuels. \"Phasing down coal is absolutely necessary, but it's not sufficient. Just because you cut coal emissions, it doesn't mean you get away with emissions in the other sectors,\" he noted. When India became the world's most populous country last year, power demand grew by 5.4% compared to 2022. This was more than double the global increase. The country's leaders have been optimistic about its path to net zero , making bold claims that 50% of its power generation will come from non-fossil fuel forms of energy by 2030. Emissions from the power sector are expected to peak around 2030, while total energy-related emissions will reach their highest around 2034, Climate Action Tracker estimated. But the Ember study showed that added pressure from droughts pushed the country to generate 78% of its electricity from fossil fuels, where coal made up 75% of that mix. Like China, India has also made significant strides in other forms of renewable energy. In 2023, India overtook Japan to become the world's third largest solar power generator, according to Ember. Ember found that India's solar power generation totaled 113 terawatt-hours (TWh) last year, representing a 145% increase since 2019. This ranks behind China (584 TWh) and the U.S. (238 TWh). \"When it comes to the pathway to carbon neutrality for China and India, you would expect the emissions to rise when demand grows. But at some point, the GDP growth needs to decouple with emissions where we need it to first peak, then fall,\" Ember's Asia Programme Director Aditya Lolla told CNBC.",
    "image_url": "https://image.cnbcfm.com/api/v1/image/107413094-1715301216475-gettyimages-1779067793-cfoto-huanengh231113_nplhs.jpeg?v=1715301302",
    "url": "http://fakeurl.com/test-article"
}

homepage_expected_result = read_json_file("tests/cnbc/article_homepage_result.json")
category_1_expected_result = read_json_file("tests/cnbc/article_category_1_result.json")

# Test function using pytest
@pytest.mark.parametrize("article_url, expected", [
    ("http://fakeurl.com/test-article", expected_result)
])
def test_scrape_article(article_url, expected):
    scraper = CNBCNewsScraper(base_url=base_url, urls_blacklist=blacklist_url)
    path_html='tests/cnbc/cnbc_article.html'
    helper_test_article(scraper, article_url, expected, path_html)
    

# Test function using pytest
@pytest.mark.parametrize("category_path, expected", [
    ("/", homepage_expected_result)  # Ensure homepage_expected_result is defined
])
def test_fetch_article_urls_homepage(category_path, expected):
    scraper = CNBCNewsScraper(base_url=base_url, urls_blacklist=blacklist_url)
    path_html = 'tests/cnbc/cnbc_homepage.html'
    helper_test_category_url_scraper(scraper, category_path, expected, path_html)
        

# Test function using pytest
@pytest.mark.parametrize("category_path, expected", [
    ("/category1", category_1_expected_result)  # Ensure homepage_expected_result is defined
])
def test_fetch_article_urls_category_1(category_path, expected):
    scraper = CNBCNewsScraper(base_url=base_url, urls_blacklist=blacklist_url)
    path_html = 'tests/cnbc/cnbc_category_1.html'
    helper_test_category_url_scraper(scraper, category_path, expected, path_html)

