from dotenv import load_dotenv
from supabase import create_client, Client
import os
import requests


class Api():
    def __init__(self):
        load_dotenv()

        SUPABASE_URL = os.getenv("SUPABASE_URL")
        SUPABASE_KEY = os.getenv("SUPABASE_KEY")
        self.supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

        self.headers = {
            'x-rapidapi-key': os.getenv("RAPIDAPI_KEY"),
            'x-rapidapi-host': os.getenv("RAPIDAPI_HOST")
        }

        self.leads = os.getenv("TABLE_LEADS")
        self.posts = os.getenv("TABLE_POSTS")
        self.final = os.getenv("TABLE_FINAL")

    def get_leads(self, username, count=float('inf')):
        """
        Fetches followers and following data for a given username from the Twitter API.
        Args:
            username (str): The Twitter username to fetch data for.
            count (int): The minimum number of followers and following to fetch. Default is all followers and following.
        Returns:
            list: A list of followers and following data.
        """
        # Define the API endpoints
        url_followers = os.getenv("API_FOLLOWERS")
        url_following = os.getenv("API_FOLLOWING")
        
        # Initialize separate querystrings for followers and following
        querystring_followers = {"screenname": username}
        querystring_following = {"screenname": username}
        
        # Initialize lists to collect followers and following data
        all_followers = []
        all_following = []
        
        # Flags to track when we've fetched all available data
        followers_complete = False
        following_complete = False

        # Fetch followers and following data until the count is met or no more data available
        while (len(all_followers) < count or len(all_following) < count) and not (followers_complete and following_complete):
            # Fetch followers if needed and not complete
            if len(all_followers) < count and not followers_complete:
                response_followers = requests.get(url_followers, headers=self.headers, params=querystring_followers)
                if response_followers.status_code == 200:
                    data_followers = response_followers.json()
                    new_followers = data_followers.get("followers", [])
                    all_followers.extend(new_followers)
                    
                    # Check if there's a cursor for pagination
                    next_cursor = data_followers.get("next_cursor")
                    if next_cursor:
                        querystring_followers["cursor"] = next_cursor
                    else:
                        followers_complete = True  # No more followers to fetch
                else:
                    followers_complete = True  # Stop on error

            # Fetch following if needed and not complete
            if len(all_following) < count and not following_complete:
                response_following = requests.get(url_following, headers=self.headers, params=querystring_following)
                if response_following.status_code == 200:
                    data_following = response_following.json()
                    new_following = data_following.get("following", [])
                    all_following.extend(new_following)
                    
                    # Check if there's a cursor for pagination
                    next_cursor = data_following.get("next_cursor")
                    if next_cursor:
                        querystring_following["cursor"] = next_cursor
                    else:
                        following_complete = True  # No more following to fetch
                else:
                    following_complete = True  # Stop on error
                    
            # Add some logging to help debug
            print(f"Current counts - Followers: {len(all_followers)}, Following: {len(all_following)}")
            
            # Break if we received no new data in this iteration
            if not new_followers and not new_following:
                print("No new data received, ending pagination")
                break

        # Combine the followers and following data
        merged_data = all_followers + all_following
        print(f"Final counts - Followers: {len(all_followers)}, Following: {len(all_following)}, Total: {len(merged_data)}")

        return merged_data


    def get_posts(self, username, cursor = None):

        url = os.getenv("API_TWEETS")
        if cursor is not None:
            querystring = {"screenname": username, "cursor": cursor}
        else:
            querystring = {"screenname": username}

        response = requests.get(url, headers = self.headers, params = querystring)
        return response.json()

