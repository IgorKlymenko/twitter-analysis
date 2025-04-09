from helper import flatten_dict, parse_date
import api
from datetime import datetime, timedelta

api = api.Api()


def save_to_supabase(data, username):
    allowed_columns = ["author_name", 'tweet_id', "bookmarks", "created_at", "favorites", "text", "lang", "quotes", "replies", "retweets", "conversation_id", "author_screen_name"]

    if data is None or not data:
        print("No data to save to Supabase. Exiting.")
        return None
    
    last_date = None
    try:
        for i in range(len(data)):
            flattened_data = flatten_dict(data[i])
            filtered_data = {k: v for k, v in flattened_data.items() if k in allowed_columns}
            filtered_data["owner"] = username

            response = api.supabase.table(api.posts).insert(filtered_data).execute()
            print("Data successfully inserted into Supabase.")
            last_date = filtered_data.get("created_at", last_date)  # Update last_date as we process

        return last_date

    except Exception as e:
        if hasattr(e, 'code') and e.code == '23505':  # Duplicate violation
            print(f"Got Duplicate. Wrapping Up {e.details}")
            return last_date  # Return the last successful date even when encountering duplicates
        print(f"Error saving to Supabase: {e}")
        return last_date  # Return the last successful date even when encountering other errors


def run_until(username, date):
    # Convert the date to a datetime object for easy comparison (using flexible date parsing)
    try:
        target_date = parse_date(date)
        # Make sure target_date is naive (without timezone)
        target_date = target_date.replace(tzinfo=None)
        print(f"Target date set to: {target_date}")
    except ValueError as e:
        print(f"Error parsing target date: {e}")
        return
    
    # Get the initial data
    try:
        data = api.get_posts(username)
        if not data or "timeline" not in data:
            print(f"No timeline data returned for {username}")
            return
            
        cursor = data.get("next_cursor")
        
        # Save initial batch and get last date
        last_date_str = save_to_supabase(data.get("timeline"), username)
        
        # If last_date is not None, convert it to a datetime object
        if last_date_str is not None:
            try:
                last_date = parse_date(last_date_str)
                last_date = last_date.replace(tzinfo=None)  # Remove timezone info
                print(f"Last processed date: {last_date}")
            except ValueError as e:
                print(f"Error parsing last date: {e}")
                last_date = None
        else:
            last_date = None
            
        # Run until the date condition is met or cursor is None
        while cursor is not None:
            # Continue fetching if we haven't reached our target date yet
            if last_date is None or last_date > target_date:
                print(f"Fetching more posts with cursor: {cursor[:20]}...")
                data = api.get_posts(username, cursor)
                
                if not data or "timeline" not in data or not data.get("timeline"):
                    print("No more data available.")
                    break
                    
                last_date_str = save_to_supabase(data.get("timeline"), username)
                
                if last_date_str:
                    last_date = parse_date(last_date_str).replace(tzinfo=None)
                    print(f"Updated last processed date: {last_date}")
                
                cursor = data.get("next_cursor")
                if not cursor:
                    print("No more pages available.")
                    break
            else:
                print(f"Target date reached. Last date {last_date} is older than or equal to target date {target_date}.")
                break
    except Exception as e:
        print(f"Error in run_until: {e}")


def main(months = 6):
    try:
        pod_lead_response = api.supabase.table(api.leads).select("screen_name").execute()

        if not pod_lead_response.data:
            print("No leads found in the database.")
            return

        for row in pod_lead_response.data:
            username = row["screen_name"]
            six_months_ago = (datetime.today() - timedelta(days=months*30)).strftime("%Y-%m-%d")
            print(f"Processing {username}, targeting posts since {six_months_ago}")
            
            try:
                run_until(username, six_months_ago)
            except Exception as e:
                print(f"Error processing {username}: {e}")
            finally:
                print(f"Completed processing for {username}")
                
        print("Twitter data retrieval process completed for all users.")
    except Exception as e:
        print(f"Error in main function: {e}")
