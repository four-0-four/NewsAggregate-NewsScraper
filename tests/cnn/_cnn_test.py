from datetime import datetime, timezone
import pytest
from unittest.mock import patch, Mock
from scraper._cnn import CNNNewsScraper
import json

from tests.test_helper import helper_test_article, helper_test_category_url_scraper, read_html_file, read_json_file
        
base_url = "https://www.cnn.com"
blacklist_url = []
        
# Expected result based on the sample HTML
expected_result = {
    'title': 'Hamas to consider ceasefire-hostage release proposal that Israeli sources say could avert Rafah invasion', 
    'date': datetime(2024, 4, 29, 17, 54, tzinfo=timezone.utc), 
    'content': " Riyadh and Jerusalem CNN — Hamas is\xa0considering\xa0a new\xa0framework\xa0proposed by Egypt\xa0that calls for the group to release as many as 33\xa0hostages\xa0kidnapped from Israel\xa0in exchange for\xa0a\xa0pause in hostilities\xa0in Gaza , an Israeli source familiar with the negotiations and a foreign diplomatic source told CNN. The latest proposal, which Israel helped craft but has not fully agreed to, is laid out in two phases, the first of which calls for 20 to 33 hostages to be released over several weeks in exchange for the pause and the release of Palestinian prisoners. The second phase is what sources described as the “restoration of sustainable calm,” during which the remaining hostages, captive Israeli soldiers and the bodies of hostages would be exchanged for more Palestinian prisoners. The diplomatic source familiar with the talks said the reference to sustainable calm was “a way to agree to a permanent ceasefire without calling it that.” After months of deadlock, agreement from both sides would be a major step toward ending the war. But a failure to agree could deepen Israel’s presence in Gaza — if no deal is made, Israel is likely to launcha large-scale ground invasion into the southern Gaza city of Rafah, where more than 1 million Palestinians are sheltering. Israel’s allies, including the United States, have warned against the operation due to the potential for large-scale civilian casualties. Relatives of Palestinian victims who lost their lives following an Israeli airstrike, take their bodies from the morgue of Rafah's El-Najar Hospital for burial on April 29, 2024. Abed Rahim Khatib/Anadolu/Getty Images Related article ‘My whole family has perished:’ 20 dead after Israeli airstrike on Rafah, hospital staff say Israel is awaiting a response from Hamas, which is expected to meet\xa0Egyptian and Qatari mediators\xa0in Cairo on Monday, the sources said. A working-level Israeli delegation of Mossad, Shin Bet and the Israeli military officials is expected to travel to Cairo on Tuesday, the Israeli source\xa0and another Israeli official\xa0said. A response from Yahya Sinwar, the Hamas leader in Gaza, is expected within days — possibly within the next 24 hours. The length of the first phase of the pause in hostilities would be linked to the number of hostages released, with the latest framework calling for a one-day pause for each hostage, the Israeli source said, although this number is expected to shift during more in-depth negotiations. The release of 40 hostages for a six-week ceasefire had been the basis of negotiations for months, but Israel has agreed to accept fewer hostages in the first phase after Hamas dropped its offer to fewer than 20 people earlier this month. ‘Extraordinarily generous’ proposal US Secretary of State Antony Blinken said on Monday that Hamas\xa0has been presented with a ceasefire proposal that is “extraordinarily generous on the part of Israel.” “In this moment the only thing standing between the people of Gaza and a ceasefire is Hamas,” he told\xa0World Economic Forum (WEF) President Børge Brende in the Saudi capital Riyadh. “They (Hamas) have to decide and they have to decide quickly,” he said. “I’m hopeful that they will make the right decision.” US Secretary of State Antony Blinken attends the US-Arab Quint Meeting with representatives from Egypt, Jordan, Saudi Arabia, Qatar, the United Arab Emirates and the Palestinian Authority, at the Four Seasons Hotel in Riyadh, Saudi Arabia on April 29. Evelyn Hockstein/Reuters Egyptian Foreign Minister Sameh Shoukry, also speaking in Riyadh, said he was hopeful that Israel and Hamas will accept the proposal. “There is a proposal on the table, up to\xa0the two sides to consider and accept but certainly the objective is a ceasefire, a permanent ceasefire and dealing with the humanitarian conditions,” Shoukry told a panel at the WEF in Riyadh on Monday. He said he is hopeful\xa0that “the proposal has been taken into account” and that “we are waiting to have a final decision.” Israeli officials have expressed an openness to negotiating the “restoration of sustainable calm” as part of a comprehensive deal that would effectively end the war. An Israeli source familiar with the negotiations said Egypt has proposed the parties agree to a one-year ceasefire as part of a comprehensive deal that would see Israeli forces withdraw from Gaza and the release of all remaining hostages and the bodies of those who have died. CNN has reached out to the Egyptian government for comment. Hamas has insisted that a permanent ceasefire and a full Israeli withdrawal from Gaza should be part of the agreement. Israel has thus far maintained that its operation in Gaza will continue until Hamas is eradicated. Israel has also now agreed to the unrestricted movement of Palestinians to northern Gaza, the sources said, a key demand by Hamas which has held back negotiations in the past. Rafah operation Hanging over the negotiations is the increasingly likely prospect of an Israeli military offensive in Rafah, which Israeli officials have signposted for months but\xa0are now holding back, saying they want to give space to the negotiations. But Israeli sources have characterized the latest Egyptian effort to broker a deal as the last chance to avert that offensive. “The only chance to stop Rafah is a deal,” the Israeli source familiar with the negotiations said. The US and other Israel allies have warned that such an operation will not have their support if adequate measures aren’t taken to ensure the safety of civilians. “Preparations for entering Rafah continue. In any deal, if there is one, Israel will not give up the goals of the war,” the Israeli official said. Blinken reiterated in Riyadh that the US wouldn’t support a major military operation in Rafah “in the absence of a plan to ensure that civilians will not be harmed”. A flotilla of aid is attempting to deliver humanitarian assistance to Gaza, in defiance of Israel who have not granted permission for them to reach the strip.  CNN's Scott McLean went aboard one of the ships and spoke to humanitarian workers about why their attempt is so risky. Clipped From Video video Related video They’re risking their lives sailing to Gaza. CNN went aboard one of the ships “We have not yet seen a plan that civilians can be effectively protected,” he said. White House National Security Council communications adviser John Kirby said Sunday that Israel has told its US counterparts that it won’t launch an invasion of\xa0Rafah\xa0until the Biden administration can share its concerns. “I think we have to have a better understanding from the Israelis about what they want to do as a matter of fact, we’ve had several staff talks with them, we intend to do that more,” he said on ABC. “They’ve assured us that they won’t go into Rafah until we’ve had a chance to really share our perspectives and our concerns with them.” In a call Sunday with Israeli Prime Minister Benjamin Netanyahu, US President Joe Biden addressed the need for increased humanitarian assistance and “reiterated his clear position” on a potential Israeli invasion of Rafah, according to a White House readout of the conversation. Rising death toll The death toll from Israel’s bombardment in Gaza continued to climb over the weekend. Twenty people, including at least one infant and a toddler, died following an Israeli airstrike over Rafah, Gaza, overnight into Monday, according to hospital officials. And in Gaza City, seven\xa0Palestinians were killed and dozens injured in two separate Israeli airstrikes overnight,\xa0Gaza\xa0Civil Defense spokesperson Mahmmoud Basal told CNN. An Israeli airstrike struck a two-story house belonging to the Tartouri family in the port area west of\xa0Gaza\xa0City, killing 5 Palestinians and wounding several others, Basal said. In a separate incident, two people were killed and several others injured when an Israeli airstrike targeted a house belonging to the Hijazi family in the Sabra neighborhood in the center of\xa0Gaza\xa0City, according to Basal. CNN’s Amy Cassidy, Abeer Salman, Kareem Khadder, Mohammed Tawfeeq and Mostafa Salem contributed to this report.", 
    'image_url': 'https://media.cnn.com/api/v1/images/stellar/prod/gettyimages-2149814371.jpg?c=16x9&q=h_833,w_1480,c_fill', 
    'url': '/2024/04/29/middleeast/hamas-israel-ceasefire-proposal-cairo-talks-intl/index.html'
}
homepage_expected_result = read_json_file("tests/cnn/article_homepage_result.json")
category_1_expected_result = read_json_file("tests/cnn/article_category_1_result.json")

# Test function using pytest
@pytest.mark.parametrize("article_url, expected", [
    ("/2024/04/29/middleeast/hamas-israel-ceasefire-proposal-cairo-talks-intl/index.html", expected_result)
])
def test_scrape_article(article_url, expected):
    scraper = CNNNewsScraper(base_url=base_url, urls_blacklist=blacklist_url)
    path_html='tests/cnn/cnn_article.html'
    helper_test_article(scraper, article_url, expected, path_html)
    

# Test function using pytest
@pytest.mark.parametrize("category_path, expected", [
    ("/", homepage_expected_result)  # Ensure homepage_expected_result is defined
])
def test_fetch_article_urls_homepage(category_path, expected):
    scraper = CNNNewsScraper(base_url=base_url, urls_blacklist=blacklist_url)
    path_html = 'tests/cnn/cnn_homepage.html'
    helper_test_category_url_scraper(scraper, category_path, expected, path_html)
        

# Test function using pytest
@pytest.mark.parametrize("category_path, expected", [
    ("/category1", category_1_expected_result)  # Ensure homepage_expected_result is defined
])
def test_fetch_article_urls_category_1(category_path, expected):
    scraper = CNNNewsScraper(base_url=base_url, urls_blacklist=blacklist_url)
    path_html = 'tests/cnn/cnn_category_1.html'
    helper_test_category_url_scraper(scraper, category_path, expected, path_html)