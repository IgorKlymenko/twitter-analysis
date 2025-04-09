from rapidfuzz import process, fuzz
import api
import json
import spacy
from spacy.cli import download
import re

# Initialize the API instance
api = api.Api()

# Try to load the spaCy model, or download it if not available
try:
    nlp = spacy.load("en_core_web_sm")
except OSError:
    print("Downloading spaCy model...")
    download("en_core_web_sm")
    nlp = spacy.load("en_core_web_sm")

# Abbreviation map for provinces, states, airports, etc.
province_abbrevs = {
    "BC": "British Columbia",
    "AB": "Alberta",
    "ON": "Ontario",
    "QC": "Quebec",
    "MB": "Manitoba",
    "SK": "Saskatchewan",
    "NS": "Nova Scotia",
    "NB": "New Brunswick",
    "NL": "Newfoundland and Labrador",
    "PE": "Prince Edward Island",
    "YEG": "Edmonton",
    "YYZ": "Toronto",
    "JFK": "New York",
    # Add more as needed
}

def fuzzy_score_text(text, keyword_tiers, threshold=85):
    """
    Calculate a fuzzy matching score for a given text based on keyword tiers.

    Args:
        text (str): The input text to be scored.
        keyword_tiers (dict): A dictionary containing keyword tiers and their respective keywords.
        threshold (int): The similarity threshold for fuzzy matching.

    Returns:
        int: The calculated score based on keyword matches.
    """
    score = 0
    for tier, keywords in keyword_tiers.items():
        for keyword in keywords:
            match, similarity, _ = process.extractOne(text, [keyword], scorer=fuzz.partial_ratio)
            if similarity >= threshold:
                tier_scores = {"tier_1": 10, "tier_2": 5, "tier_3": 2}
                score += tier_scores.get(tier, 0)
    return score

def get_all_tweets():
    """
    Fetch all tweets from the database using pagination.

    Returns:
        list: A list of tweets containing text, owner, author_screen_name, and created_at.
    """
    start = 0
    batch_size = 100
    all_tweets = []

    while True:
        response = api.supabase.table(api.posts).select("text", "owner", "author_screen_name", "created_at").range(start, start + batch_size - 1).execute()
        if not response.data:
            break
        all_tweets.extend(response.data)
        start += batch_size

    return all_tweets

def refine_location(location):
    """
    Refine a location string by detecting entities and mapping abbreviations.

    Args:
        location (str): The input location string.

    Returns:
        str: The refined location string or None if input is invalid.
    """
    if location:
        doc = nlp(location)
        location_tokens = []
        token_positions = []

        for ent in doc.ents:
            if ent.label_ in ["GPE", "LOC", "NORP", "FAC"]:
                location_tokens.append(ent.text)
                token_positions.append((ent.start_char, ent.end_char))

        for token in location.split():
            if token.upper() in province_abbrevs:
                location_tokens.append(province_abbrevs[token.upper()])
                token_positions.append((location.index(token), location.index(token) + len(token)))

        result = ""
        last_index = 0
        for start, end in token_positions:
            if start > last_index:
                result += location[last_index:start]
            result += location[start:end]
            last_index = end

        return result.strip()
    return None

def get_companies(description, keywords):
    """
    Identify company names in a description based on a list of keywords.

    Args:
        description (str): The input description text.
        keywords (dict): A dictionary containing company-related keywords.

    Returns:
        str: A space-separated string of identified company names or None if no matches are found.
    """
    identified_companies = []
    for company in keywords["companies"]:
        escaped_company = re.escape(company)
        pattern = r'\b' + escaped_company + r'\b'
        matches = re.findall(pattern, description, re.IGNORECASE)
        identified_companies.extend(matches)
    return ' '.join(identified_companies) if identified_companies else None

def main():
    """
    Main function to process tweets, calculate attractiveness scores, and update lead data.

    This function performs the following tasks:
    1. Loads keywords from a JSON file.
    2. Fetches all tweets using pagination.
    3. Calculates attractiveness scores for each tweet owner based on the presence of specific keywords.
    4. Identifies additional attributes such as whether the owner is a founder, Canadian, or a venture capitalist (VC).
    5. Retrieves existing lead records from the database and updates them with new data.
    6. Uploads the combined lead data back to the database.

    Returns:
        None
    """
    with open("../data/keywords.json", "r") as file:
        keywords = json.load(file)

    all_tweets = get_all_tweets()
    attractiveness_dict = {}

    for row in all_tweets:
        text = row["text"]
        screen_name = row["owner"]
        author_screen_name = row["author_screen_name"]

        if screen_name not in attractiveness_dict:
            attractiveness_dict[screen_name] = 0.0

        most_recent_tweet = None

        if screen_name == author_screen_name:
            attractiveness_dict[screen_name] += 0.2 * fuzzy_score_text(text, keywords["keyword_tiers"])
        else:
            attractiveness_dict[screen_name] += 0.1 * fuzzy_score_text(text, keywords["keyword_tiers"])

        most_recent_tweet = text

        applied = any(word in keywords["applied"] for word in text)
        ventures = [text for word in text if applied and word in keywords["ventures"]]

        founder = any(keyword.lower() in text.lower() for keyword in keywords["founder_keywords"])
        canadian = any(keyword.lower() in text.lower() for keyword in keywords["canadian_keywords"])
        vc = any(keyword.lower() in text.lower() for keyword in keywords["vc_keywords"])

        pod_lead_response = api.supabase.table(api.leads).select("*").eq("screen_name", screen_name).execute()

        if pod_lead_response.data:
            pod_lead = pod_lead_response.data[0]

            if pod_lead.get("description"):
                description = pod_lead["description"].lower()
                if any(keyword.lower() in description for keyword in keywords["founder_keywords"]):
                    founder = True

            if pod_lead.get("location"):
                location = pod_lead["location"].lower()
                if any(keyword.lower() in location for keyword in keywords["canadian_keywords"]):
                    canadian = True

            if pod_lead.get("description"):
                description = pod_lead["description"].lower()
                if any(keyword.lower() in description for keyword in keywords["vc_keywords"]):
                    vc = True

            location = refine_location(pod_lead["location"])

            lead_data = {
                "owner": screen_name,
                "tweet": most_recent_tweet,
                "score": attractiveness_dict[screen_name],
                "founder": founder,
                "canadian": canadian,
                "vc": vc,
                "location": location,
                "ventures": ventures,
                "companies": get_companies(pod_lead["description"], keywords)
            } if most_recent_tweet else {
                "owner": screen_name,
                "score": attractiveness_dict[screen_name],
                "founder": founder,
                "canadian": canadian,
                "vc": vc,
                "location": location,
                "ventures": ventures,
                "companies": get_companies(pod_lead["description"], keywords)
            }

            combined_lead_data = {**pod_lead, **lead_data}
            upload_response = api.supabase.table(api.final).upsert(combined_lead_data).execute()

            print(f"Lead updated successfully for {screen_name} with accumulated score {attractiveness_dict[screen_name]}")
        else:
            print(f"No pot_leads found for {screen_name}. Skipping update.")
