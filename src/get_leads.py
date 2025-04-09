import csv
import re
from helper import flatten_dict
import api

# Initialize the API instance
api = api.Api()

def clean_data(user_data):
    """
    Cleans user data by converting string numbers to integers, 
    boolean strings to booleans, and 'None' strings to None.

    Args:
        user_data (dict): Dictionary containing user data.

    Returns:
        dict: Cleaned user data.
    """
    for key in ["statuses_count", "followers_count", "friends_count", "media_count"]:
        user_data[key] = int(user_data[key]) if user_data[key].isdigit() else None

    return user_data


def save_to_supabase(data):
    """
    Saves the provided data to a Supabase table after cleaning and filtering.

    Args:
        data (list): List of dictionaries containing user data.

    Returns:
        None
    """
    allowed_columns = [
        "user_id", "screen_name", "description", "profile_image",
        "statuses_count", "followers_count", "friends_count",
        "media_count", "created_at", "location", "blue_verified", 
        "website", "name", "business_account"
    ]

    if data is None:
        print("No data to save to Supabase. Exiting.")
        return

    for i in range(len(data)):
        # Flatten nested dictionaries
        flattened_data = flatten_dict(data[i])
        # Filter only allowed columns
        filtered_data = {k: v for k, v in flattened_data.items() if k in allowed_columns}
        # Clean the data
        cleaned_data = clean_data(filtered_data)

        try:
            # Insert data into Supabase
            response = api.supabase.table(api.leads).insert(cleaned_data).execute()
            print("Data successfully inserted into Supabase.")
        except Exception as e:
            # Handle duplicate entry errors
            if hasattr(e, 'code') and e.code == '23505':  # Duplicate violation
                print(f"Data already exists in the table: {e.details}")
                continue
            else:
                print(f"An error occurred while saving to Supabase: {e}")
                break


def main(DATAFILE="../data/leads.csv", count=float('inf')):
    """
    Main function to process the input CSV file, extract leads, 
    and save them to Supabase.

    Args:
        DATAFILE (str): Path to the input CSV file.
        count (int): Number of leads to fetch per user (default: all).

    Returns:
        None
    """
    with open(DATAFILE, 'r', newline='', encoding='utf-8') as file:
        reader = csv.reader(file)
        for row in reader:
            if len(row) > 1:
                # Extract Twitter username from the profile URL
                match = re.search(r"x\.com/([^/]+)", row[1])

                if match:
                    print(match.group(1)) 
                    # Fetch leads using the API
                    data = api.get_leads(match.group(1), count)  # Default is all followers/following
                    print(len(data))
                    # Save the data to Supabase
                    save_to_supabase(data)