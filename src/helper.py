from datetime import datetime

def flatten_dict(d, parent_key='', sep='_'):
    """
    Recursively flattens a nested dictionary, including nested lists of dictionaries, 
    into a single-level dictionary with keys representing the hierarchy.
    Args:
        d (dict): The dictionary to flatten.
        parent_key (str, optional): A prefix for the keys in the flattened dictionary. Defaults to ''.
        sep (str, optional): The separator to use between levels of the hierarchy in the keys. Defaults to '_'.
    Returns:
        dict: A flattened dictionary where nested keys are concatenated with the specified separator.
    Notes:
        - If a key starts with "retweeted_tweet_", this prefix is removed in the flattened dictionary.
        - Nested lists are handled by appending the index of the list item to the key.
        - All non-dictionary and non-list values are converted to strings in the flattened dictionary.
    """
    items = []
    for k, v in d.items():
        # Adjust key by removing "retweeted_tweet_" if it exists
        new_key = f"{parent_key}{sep}{k}" if parent_key else k
        if new_key.startswith("retweeted_tweet_"):
            new_key = new_key.replace("retweeted_tweet_", "", 1)
        
        if isinstance(v, dict):
            items.extend(flatten_dict(v, new_key, sep=sep).items())
        elif isinstance(v, list):
            for i, item in enumerate(v):
                if isinstance(item, dict):
                    items.extend(flatten_dict(item, f"{new_key}{sep}{i}", sep=sep).items())
                else:
                    items.append((f"{new_key}{sep}{i}", str(item)))
        else:
            items.append((new_key, str(v)))
    return dict(items)

def parse_date(date_str):
    """Parses the date string in multiple formats."""
    date_formats = [
        "%Y-%m-%d",                # 2024-08-01
        "%a %b %d %H:%M:%S %z %Y",  # Sun Oct 27 18:38:58 +0000 2024
        "%Y-%m-%dT%H:%M:%SZ",      # 2024-08-01T00:00:00Z
        "%d/%m/%Y",                # 27/10/2024
        "%m/%d/%Y",                # 10/27/2024
        "%Y-%m-%dT%H:%M:%S",       # 2025-04-07T22:34:11
    ]
    
    for fmt in date_formats:
        try:
            return datetime.strptime(date_str, fmt)
        except ValueError:
            continue
    
    raise ValueError(f"Date format for '{date_str}' is not supported")