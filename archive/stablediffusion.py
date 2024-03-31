import requests

news = "Toronto FC\u2019s home-opening 1-0 win Saturday over Charlotte FC was filled with milestones for captain Jonathan Osorio. The game marked Osorio\u2019s 300th in MLS regular-season and playoff action. And it came 11 years to the day from his debut for his hometown club, replacing Terry Dunfield \u2014 now a TFC assistant coach under John Herdman \u2014 in the 82nd minute of a 2-1 win over Sporting Kansas City at Rogers Centre. Osorio was not dwelling on the past, however. \u201cI was in the moment,\u201d he said when asked about the milestones, which he said he didn\u2019t know until he was apprised of them after the game. \u201cThat\u2019s all great, but honestly all that I really care about is that we won our home opener and we keep in a good way,\u201d he added. Story continues below advertisement The Charlotte win, TFC\u2019s third straight clean sheet, moved Toronto (2-0-1, seven points) into sixth place overall in Major League Soccer. Quite the turnaround for the league\u2019s worst team last season (4-20-10, 22 points). Osorio comes from a city replete with sporting leadership. Leafs captains include the likes of Hap Day, Syl Apps, Ted (Teeder) Kennedy, George Armstrong, Dave Keon, Darryl Sittler, Rick Vaive, Wendel Clark, Doug Gilmour, Mats Sundin and John Tavares, TFC\u2019s captains\u2019 tree is far shorter: Jim Brennan, Dwayne De Rosario, Maicon Santos, Torsten Frings, Darren O\u2019Dea, Steven Caldwell and Michel Bradley. More on Sports Blue Jays roll to spring training win over Philly Votto agrees to non-roster invite with Jays Lukes\u2019 two-run triple leads Blue Jays over Yankees Blue Jays top Tigers 5-4 in pre-season action But Herdman, who coached Osorio with Canada, says the midfielder was key to his decision to leaving the national team to take over TFC on Oct. 1. The email you need for the day's top news stories from Canada and around the world. \u201cI\u2019ve worked with (Christine) Sinclair, I\u2019ve worked with Atiba Hutchinson. Just some great people, some great humans. And they\u2019re right in the core of your leadership group,\u201d Herdman said. \u201cAnd if you\u2019ve got a player with that character, that high-level character, like highest-standard character, you want to work with these people. \u201cSo for me, the conversation coming to TFC (was) \u201dAre you going to be there? Are you committed? Will you wear the armband? Are you committed to taking this club back \u2014 and beyond where it was at?\u2019 And he was.\u201d Herdman calls his captain, known simply as Oso, \u201cthe hardest-working player on the team.\u201d Story continues below advertisement \u201cYou see his quality as well. He\u2019s going to do all that selfless running. But he can bring the quality in those moments as well.\u201d Herdman also approvingly repeated Osorio\u2019s words Saturday. \u201cWhat he said at the end of this (game) sort of summarizes him \u2014 \u2018It\u2019s just another step, guys. Just one more step to bringing this club to where it needs to be.'\u201d \u201cAnd that\u2019s his mentality,\u201d Herdman added. \u201cHe\u2019s always on. Next step, next step, next step. He\u2019s never thinking about the last step and he\u2019s never willing to stand and wait to be pushed. He\u2019s pushing everyone.\u201d Today, Osorio leads the club in appearances at 344 in all competitions, ranks third in goals at 62 (behind Sebastian Giovinco\u2019s 83 and Jozy Altidore\u2019s 79) and second in assists at 50 (behind Giovinco\u2019s 52). Trending Now Kate Middleton appears in first photo since surgery amid wild speculation of whereabouts The rock star who defected to North Korea \u2014 and now regrets it Credit former coach Ryan Nelsen for identifying Osorio as a player to watch early in camp prior to the 2013 season and then gave him his chance to show it. \u201cNothing fazes him. Not even bad moments in games,\u201d Nelsen said in August 2013. \u201cHe always tries to do things positively. Instead of going into his shell, he tries to keep doing stuff. And I love that because the game and life in general rewards those people.\u201d Story continues below advertisement Osorio took the long road to his hometown club, spending two years as a teenager \u2014 along with longtime friend and fellow Canadian international Lucas Cavallini \u2014 at Club Nacional in Montevideo, Uruguay. He played in the under-19 ranks and reserves before coming home at the end of 2011. While both he and Cavallini spoke the language \u2014 Osorio\u2019s parents were born in Colombia while Cavallini\u2019s father is originally from Argentina \u2014 they were not welcome at first. They lived in dormitory-style accommodations with Uruguayan juniors initially seeing them as foreign intruders looking to take their jobs. \u201cIt was so crucial to me becoming the person and the player that I am now. I owe Uruguay so much, I\u2019ll never forget my time there,\u201d Osorio said in a 2022 interview. He joined TFC\u2019s academy in September 2012 after impressing in the Canadian Soccer League. In February 2013 he was at Toronto\u2019s camp in Florida and was included in Nelsen\u2019s first starting 11. He has never left, signing his existing contract in December 2022, a three-year deal with a club option for 2026. His salary of US$1.4 million last season ranked him third on the club behind Italians Lorenzo Insigne (US$15.4 million) and Federico Bernardeschi (US$6.295 million). Fluent in Spanish, Osorio is equally adept at connecting off the pitch as he is on it. Advertisement"


api = "7rTSZ5vBbK16GjuSbWMmQhmvYaw5NJQmCpNzPpac52FumYbjbJw0hc2rMD0G"
url = "https://modelslab.com/api/v5/uncensored_chat"


async def get_news_summary(title,content):
    news = title + " - " + content
    headers = {"Content-Type": "application/json"}
    data = {
        "key": api,
        "messages": [
            {
                "role": "user",
                "content": """summarize the news below. at most 300 words and break into paragraphs if necessary. 
                make sure the summary is understandable, contains most of the details and has a good flow <NEWS>"""+news+"""</NEWS>"""
            }
        ],
        "max_tokens": 1000
    }

    response = requests.post(url, json=data, headers=headers)
    data = response.json()
    if response.status_code == 200 and data["status"] == "success":
        return data["message"]
    return None


async def get_news_ner(text):
    news = text
    headers = {"Content-Type": "application/json"}
    data = {
        "key": api,
        "messages": [
            {
                "role": "user",
                "content": """"Extract most relevant and most entities from the following news article. Provide the full names of these entities for clarity. please provide the category of each entity in one or two words for better classification. no explanation is required. put the entities in a json file with columns/keys entity and type. please provide the json only and no other explanation for response. provide the full name of entities and no abbreviation(as much possible). put the entities inside the json with keys "entity" and "category". Here's the news article for analysis:    <NEWS>"""+news+"""</NEWS>"""
            }
        ],
        "max_tokens": 1000
    }

    response = requests.post(url, json=data, headers=headers)
    data = response.json()
    if response.status_code == 200 and data["status"] == "success":
        return data["message"]
    return None


#text = " The Bahais, Iran's largest non-Muslim religious minority, face persecution even after death. In Khavaran cemetery, graves of at least 30 Bahais were destroyed and their resting places levelled by Iranian authorities, according to the Bahai International Community (BIC). This is another attack on the Bahais, who have been subjected to systematic persecution and discrimination since the foundation of the Islamic republic in 1979. The BIC claims that Bahai-owned burial sites were confiscated after the 1979 Islamic revolution and their dead are now forcibly buried in Khavaran, where political prisoners executed in 1988 are also buried. The desecration of the graves has been condemned by the United States and United Nations officials. Bahais are not allowed to have their faith recognised by Iran's constitution, nor are they granted any special representation in parliament or access to higher education. They face harassment ranging from raids against their businesses to confiscation of assets and arrests. Khavaran's destruction comes at a time when Bahai persecution is intensifying in Iran; two senior community figures were arrested in July 2022 and are each serving 10-year jail sentences, and hundreds more are in detention or facing court proceedings. The Bahai faith dates back to the early 19th century in Iran and has a spiritual centre in Haifa, Israel. Critics claim Bahais are charged with being agents of Iran's arch-foe, Israel, although these accusations are without foundation. The intensified repression of the Bahais is linked to the nationwide protests that erupted in September 2022, as the authorities seek to crush all forms of dissent. The UN special rapporteur on human rights in Iran, Javaid Rehman, expressed his distress and shock at the ongoing persecution of the Bahais. Bahais have faced a range of intimidation and violence throughout the past several decades, with at least 200 of them executed in the aftermath of the Islamic revolution."

#loop = asyncio.get_event_loop()
#res = loop.run_until_complete(get_news_summary2(text))
#res = loop.run_until_complete(get_news_ner(text))
#print(res)

#res2 = loop.run_until_complete(get_news_entities_claude(text))
#print("###############################################################")
#print(res2)