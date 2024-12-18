from datetime import datetime
import pytest
from unittest.mock import patch, Mock
from scraper._nbc import NBCNewsScraper
import json

from tests.test_helper import helper_test_article, helper_test_category_url_scraper, read_html_file, read_json_file
        
base_url = "https://www.nbcnews.com/"
blacklist_url = []
        
# Expected result based on the sample HTML
expected_result = {
    'title': "2024 NFL draft: Top prospects, storylines to watch ahead of Thursday's first round", 
    'date': datetime(2024, 4, 25, 18, 41, 52, 313000), 
    'content': " The first round of the 2024 NFL draft takes place Thursday at 8 p.m. in Detroit, a night that could alter the future of many franchises. The Chicago Bears, Washington Commanders and New England Patriots own the top three selections, and many speculate those picks going to quarterbacks, which has happened three other times, most recently in 2021. Leila Register / NBC News; Getty Images USC signal-caller Caleb Williams is all but certain to go No. 1, so the intrigue officially starts with Washington. Which quarterback will the new general manager, Adam Peters, take? That’s just one of the many storylines to watch on ABC, ESPN or the NFL Network. Is Williams guaranteed to go to Chicago? Nothing is guaranteed until NFL Commissioner Roger Goodell steps up to the podium and reads his name but, essentially, yes. Follow along for live coverage of the NFL d raft Williams, the consensus top prospect, threw for 3,633 yards, 30 touchdowns and five interceptions last season. He won the Heisman Trophy as the best player in college football the prior year after taking the Trojans from four wins to an 11-win team. Williams threw for 4,075 yards, 37 touchdowns and only four interceptions over 13 games in 2022. More Sports from NBC News Pacers' star Tyrese Haliburton says rival fan directed racist slur at his brother during playoff game After $1.5 billion was spent, the centerpiece of Paris' Olympic efforts may still be too filthy to use Simone Biles on Olympics twisties: 'I thought I was going to be banned from America' He will join a retooled Chicago team that traded for six-time Pro Bowl receiver Keenan Allen and signed running back D’Andre Swift in free agency this offseason. Williams will also be able to throw the ball to rising stars in receiver D.J. Moore and tight end Cole Kmet. What will the Commanders do at No. 2? Like the Bears, the Commanders have been desperate for a franchise quarterback for more than three decades. There was a glimmer of hope with Robert Griffin III, the 2012 NFL Offensive Rookie of the Year, but multiple injuries over the next seven seasons led to an early exit from the league. Will this finally be Washington’s chance to turn around the franchise? The Commanders have a new owner in Josh Harris and a new general manager in Peters, and both have been tight-lipped on whom they might select. But all signs point to either LSU quarterback Jayden Daniels or University of North Carolina quarterback Drake Maye. North Carolina quarterback Drake Maye during the first half of an NCAA college football game in Clemson, N.C., in November. Jacob Kupferman / AP file The 6-foot-4, 210-pound Daniels won the 2023 Heisman Trophy after one of the most electrifying seasons in college football history. He threw for 3,812 yards, 40 touchdowns and only four interceptions, while also adding 1,134 yards and 10 touchdowns on the ground. Maye, at 6-foot-4 and 230 pounds, boasts the prototypical size for the position and has drawn comparisons to Los Angeles Chargers signal-caller Justin Herbert. After being named 2022 ACC Player and Rookie of the Year as a sophomore, he threw for 3,608 yards, 24 touchdowns and nine interceptions as a junior. University of Michigan quarterback J.J. McCarthy, who led the Wolverines to their first national title since 1997, is also reportedly being considered. Patriots could look to trade down New England is still looking to find a replacement for legendary quarterback Tom Brady, who left the franchise in 2019. Mac Jones, a first-round pick in 2021, looked promising as a rookie but saw production drop off over the last two seasons. He was dealt to the Jacksonville Jaguars this offseason. The Patriots signed Jacoby Brissett, though he’s not expected to be the long-term starter. Will they instead take whoever is left among  Daniels, Maye and McCarthy? If not, a trade down with a team such as the New York Giants, Minnesota Vikings or Las Vegas Raiders could be in play. All are searching for a quarterback and would give up a multitude of picks to secure that. The Patriots, who finished 4-13 last season and has holes all over the roster, could use those extra picks to expedite a rebuild. Which wide receiver will go first? For much of the past year, Ohio State receiver Marvin Harrison Jr. has been the presumptive top wideout available. It’s still likely he is the first pass-catcher off the board, but LSU’s Malik Nabers and the University of Washington’s Rome Odunze have reportedly seen their stock rise enough this offseason to make it a competition. Harrison, the son of longtime Indianapolis Colts star receiver Marvin Harrison, is arguably the greatest receiver in Ohio State history. He won the Biletnikoff Award last season as the most outstanding receiver in college football after catching 67 passes for 1,211 yards and 14 touchdowns. Nabers will look to become the next star receiver from LSU, joining the likes of Justin Jefferson, Ja’Marr Chase and Odell Beckham Jr. The 6-foot, 199-pound Nabers catches everything in sight and will provide a team with instant playmaking ability. He hauled in 89 passes for 1,569 yards and 14 scores. LSU wide receiver Malik Nabers during a game against the Grambling State in Baton Rouge, La., on Sept. 9. Jonathan Mailhes / Cal Sport Media via AP file Odunze, at 6-foot-3, 215 pounds, possesses elite size for the position. He set a program record with 1,640 receiving yards last season, the highest total in the country and the third-most ever in the Pac-12. Defensive players expected to wait Generally speaking, this draft is known for elite offensive prospects. We could see five quarterbacks, six receivers and potentially double-digit offensive linemen picked in the first 32 selections. But let’s not forget about a few defensive studs. Pass rushers Dallas Turner (University of Alabama) and Jared Verse (Florida State) as well as defensive tackle Byron Murphy III (University of Texas) will all be in the mix to come off the board early. Sad night for Panthers fans The Carolina Panthers finished last season with a league-worst 2-15 record. Top pick and quarterback Bryce Young struggled mightily as a rookie (though he didn’t have much to work with) and the team has many areas of concern. They should have the No. 1 pick in the draft for a chance to turn around the franchise, but alas … they have zero first-round selections. Carolina surrendered Moore, 2023 first- and second-round picks, a 2024 first-round pick and a 2025 second-round pick for the chance to take Young last year. If he doesn’t improve quickly, and that’s a big if, it will go down as one of the worst trades in NFL history. Panthers fans can probably just take Thursday night off.", 
    'image_url': 'https://media-cldnry.s-nbcnews.com/image/upload/t_fit-760w,f_auto,q_auto:best/rockcms/2024-04/240423-nfl-draft-primer-lr-17b5fc.jpg', 
    'url': 'https://abcnews.go.com/International/wireStory/russian-journalist-detained-posts-criticizing-military-lawyer-109687612'
}

homepage_expected_result = read_json_file("tests/nbc/article_homepage_result.json")
category_1_expected_result = read_json_file("tests/nbc/article_category_1_result.json")

# Test function using pytest
@pytest.mark.parametrize("article_url, expected", [
    ("https://abcnews.go.com/International/wireStory/russian-journalist-detained-posts-criticizing-military-lawyer-109687612", expected_result)
])
def test_scrape_article(article_url, expected):
    scraper = NBCNewsScraper(base_url=base_url, urls_blacklist=blacklist_url)
    path_html='tests/nbc/nbc_article.html'
    helper_test_article(scraper, article_url, expected, path_html)
    

# Test function using pytest
@pytest.mark.parametrize("category_path, expected", [
    ("/", homepage_expected_result)  # Ensure homepage_expected_result is defined
])
def test_fetch_article_urls_homepage(category_path, expected):
    scraper = NBCNewsScraper(base_url=base_url, urls_blacklist=blacklist_url)
    path_html = 'tests/nbc/nbc_homepage.html'
    helper_test_category_url_scraper(scraper, category_path, expected, path_html)
        

# Test function using pytest
@pytest.mark.parametrize("category_path, expected", [
    ("/category1", category_1_expected_result)  # Ensure homepage_expected_result is defined
])
def test_fetch_article_urls_category_1(category_path, expected):
    scraper = NBCNewsScraper(base_url=base_url, urls_blacklist=blacklist_url)
    path_html = 'tests/nbc/nbc_category_1.html'
    helper_test_category_url_scraper(scraper, category_path, expected, path_html)
