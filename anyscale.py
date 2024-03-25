from collections import Counter
import openai
import re


client = openai.OpenAI(
    base_url = "https://api.endpoints.anyscale.com/v1",
    api_key = "esecret_4975vlked3sj5uf664jx5bq4rn"
)

models = {
    1: "mistralai/Mistral-7B-Instruct-v0.1",
    2: "mlabonne/NeuralHermes-2.5-Mistral-7B",
    3: "Open-Orca/Mistral-7B-OpenOrca",
    4: "HuggingFaceH4/zephyr-7b-beta",
    5: "google/gemma-7b-it"
}

CATEGORIES_TABLE = {
    0: 'Politics',
    1: 'Business & Economy',
    2: 'Health',
    3: 'Art & Culture',
    4: 'Technology',
    5: 'Science',
    6: 'Society & Lifestyle',
    7: 'Sports',
    8: 'Environment',
}
CATEGORIES_STR = "CATEGORIES_TABLE = {0: 'Politics', 1: 'Business & Economy', 2: 'Health', 3: 'Art & Culture', 4: 'Technology', 5: 'Science', 6: 'Society & Lifestyle', 7: 'Sports', 8: 'Environment',}"

############################################################  anyscale calls

def summarize_anyscale(text):
    # Note: not all arguments are currently supported and will be ignored by the backend.
    query = "summarize the news below. at most 300 words and break into paragraphs if necessary. make sure the summary is understandable, contains most of the details and has a good flow. Here is the news: <NEWS>"+text+"</NEWS>"
    system_prompt = "summarize the news below. at most 300 words and break into paragraphs if necessary. make sure the summary is understandable, contains most of the details and has a good flow. provide as much detail as possible in the summary"
    chat_completion = client.chat.completions.create(
        model=models[2],
        messages=[{"role": "system", "content": system_prompt}, 
                {"role": "user", "content": query}],
        temperature=0.5
    )
    return chat_completion.choices[0].message.content


def categorize_anyscale(text, model_number):
    # Note: not all arguments are currently supported and will be ignored by the backend.
    query = f"""between the categories provided {CATEGORIES_STR} which category the following news belong to? please provide the index of category for answer and do not provide explanation for why you chose the category.just respond with the index of category. Here's the news article for analysis: <NEWS>{text}</NEWS>"""
    system_prompt = "classify the category of the news. please provide the index of category for answer and do not provide explanation for why you chose the category. "
    chat_completion = client.chat.completions.create(
        model=models[model_number],
        messages=[{"role": "system", "content": system_prompt}, 
                {"role": "user", "content": query}],
        temperature=0.1
    )
    return chat_completion.choices[0].message.content


############################################################  helper functions

def find_category_in_text(text, categories):
    # Use a regular expression to find all occurrences of integers in the text
    numbers = re.findall(r'\d+', text)
    
    # Convert the found strings into integers
    integers = [int(number) for number in numbers]
    
    # Return the first integer if the list is not empty; otherwise, return None
    return integers[0] if integers else None
    
    

def parse_category_until_ok(text, model_number):
    category_response = categorize_anyscale(text, model_number)
    potential_category_index = find_category_in_text(category_response, CATEGORIES_TABLE)
    while not isinstance(potential_category_index, int):
        print("WARNING: The model did not provide a valid category. Please try again.")
        category_response = categorize_anyscale(text, model_number)
        potential_category_index = find_category_in_text(category_response, CATEGORIES_TABLE)
    return potential_category_index



def predict_category(text: str):
    predicted_category_1 = parse_category_until_ok(text, 3)
    
    predicted_category_2 = parse_category_until_ok(text, 5)

    if predicted_category_1 == predicted_category_2:
        return predicted_category_1


    predicted_category_3 = parse_category_until_ok(text, 4)
    
    # Aggregate the results and decide the final category
    categories = [predicted_category_1, predicted_category_2, predicted_category_3]
    categories_filtered = [cat for cat in categories if cat is not None]

    # Use Counter to find the most common category among the predictions
    if categories_filtered:
        most_common_category, count = Counter(categories_filtered).most_common(1)[0]
        
        # Check if the most common category is clearly more common than the others
        if count > 1:
            final_category = most_common_category
        else:
            # If there's no clear consensus (e.g., all categories are different),
            # fallback to Claude's response
            final_category = predicted_category_2
    else:
        # If no categories were predicted (all were None), you might want to define a default behavior
        final_category = None  # or any other default action

    return final_category


#news = """In Iran, Bahai minority faces persecution even after death\nParis (AFP) – A flattened patch of earth is all that remains of where the graves once stood –- evidence, Iran's Bahais say, that their community is subjected to persecution even in death.\n\nIssued on: 22/03/2024 - 11:57\nModified: 22/03/2024 - 11:56\n\n3 min\nOne of the Bahai faith's major temples is in Haifa, Israel, although its spiritual roots are in 19th century Iran\nOne of the Bahai faith's major temples is in Haifa, Israel, although its spiritual roots are in 19th century Iran © RONALDO SCHEMIDT / AFP/File\nBeneath the ground in the Khavaran cemetery in the southeastern outskirts of Tehran lie the remains of at least 30 and potentially up to 45 recently-deceased Bahais, according to the Bahai International Community (BIC).\n\nBut their resting places are no longer marked by headstones, plaques and flowers, as they once were, because, said the BIC, this month Iranian authorities destroyed them and then levelled the site with a bulldozer.\n\nThe desecration of the graves represents a new attack against Iran's biggest non-Muslim religious minority which has, according to its representatives, been subjected to systematic persecution and discrimination since the foundation of the Islamic republic in 1979.\n\nThe alleged destruction has been condemned by the United States, which has also criticised the ongoing persecution of the Bahais, as have United Nations officials.\n\nUnlike other minorities, Bahais do not have their faith recognised by Iran's constitution and have no reserved seats in parliament. They are unable to access the country's higher education and they suffer harassment ranging from raids against their businesses to confiscation of assets and arrest.\n\nEven death does not bring an end to the persecution, the BIC says.\n\nAccording to the community, following the 1979 Islamic revolution in Iran, the authorities confiscated two Bahai-owned burial sites and now forcibly bury their dead in Khavaran.\n\nThe cemetery is the site of a mass grave where political prisoners executed in 1988 are buried.\n\n"They want to put pressure on the Bahai community in every way possible," Simin Fahandej, the BIC representative to the United Nations, told AFP.\n\n"These people have faced persecution all their lives, were deprived of the right to go to university, and now their graves are levelled."\n\nThe US State Department's Office of International Religious Freedom said it condemned the "destruction" of the graves at the cemetery, adding that Bahais "in Iran continue to face violations of funeral and burial rights".\n\n'Going after the dead'\nThe razing of the graves comes at a time of intensified repression of the Bahai community in Iran, which representatives believe is still hundreds of thousands strong.\n\nSenior community figures Mahvash Sabet, a 71-year-old poet, and Fariba Kamalabadi, 61, were both arrested in July 2022 and are serving 10-year jail sentences.\n\nBoth were previously jailed by the authorities in the last two decades.\n\n"We have also seen the regime dramatically increase Bahai property seizures and use sham trials to subject Bahais to extended prison sentences," said the US State Department.\n\nAt least 70 Bahais are currently in detention or are serving prison sentences, while an additional 1,200 are facing court proceedings or have been sentenced to prison sentences, according to the United Nations.\n\nThe Bahai faith is a relatively young monotheistic religion with spiritual roots dating back to the early 19th century in Iran.\n\nMembers have repeatedly faced charges of being agents of Iran's arch-foe Israel, which activists say are without any foundation.\n\nThe Bahais have a spiritual centre in the Israeli port city of Haifa, but its history dates back to well before the establishment of the state of Israel in 1948.\n\n"The fact that they are going after the dead shows that they are motivated by religious persecution and not by a perceived threat to national security or society," said Fahandej.\n\nRepression of the Bahais, 200 of whom were executed in the aftermath of the Islamic revolution, has varied in strength over the last four-and-a-half decades but has been in one of its most intense phases in recent years, community members and observers say.\n\nThe UN special rapporteur on human rights in Iran, Javaid Rehman, told the UN Human Rights Council in Geneva this week he was "extremely distressed and shocked at the persistent persecution, arbitrary arrests and harassment of members of the Bahai community".\n\nFahandej said it was not clear what had prompted the current crackdown but noted it came as the authorities seek to stamp out dissent of all kinds in the wake of the nationwide protests that erupted in September 2022.\n\n"The treatment of the Bahais is very much connected with the overall situation of human rights in the country," she said."""
#print(predict_category(news))