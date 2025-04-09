# General DB Structure  
## 3-table Database  
- `leads`  
- `posts`  
- `final`  

---

## leads  
- `user_id`: unique user ID  
- `screen_name`: username  
- `description`: profile description  
- `profile_image`: profile picture URL  
- `statuses_count`: total number of Tweets (including retweets)  
- `followers_count`: number of followers  
- `friends_count`: number of users they follow  
- `media_count`: total number of times a tweet's media content (images, GIFs, or videos) has been viewed  
- `created_at`: when we scraped the profile for the first time  
- `location`: profile location field  
- `blue_verified`: whether the account has the blue checkmark  
- `website`: personal or company website  
- `name`: full name  
- `business_account`: whether it’s a business account  

---

## posts  
- `tweet_id`: unique post ID  
- `bookmarks`: number of bookmarks  
- `created_at`: when we scraped the post for the first time  
- `favorites`: number of likes  
- `text`: textual content of the tweet  
- `lang`: language of the tweet  
- `quotes`: number of quote tweets  
- `replies`: number of replies  
- `retweets`: number of retweets  
- `conversation_id`: unique comment thread ID  
- `author_name`: name of the original author  
- `author_screen_name`: username of the original author  
- `owner`: username of the person who reposted/shared the tweet  

---

## final  
- `user_id` (bigint, not null): unique user ID  
- `screen_name` (text, not null): username  
- `description` (text, null): profile description  
- `profile_image` (text, null): profile picture URL  
- `statuses_count` (integer, null): total number of Tweets (including retweets)  
- `followers_count` (integer, null): number of followers  
- `friends_count` (integer, null): number of users they follow  
- `tweet` (text, null): most recent relevant tweet  
- `media_count` (integer, null): number of media tweets or total media views  
- `created_at` (timestamp with time zone, null): when we scraped the user for the first time  
- `location` (text, null): profile location field (after the `filter.py` rewrote it in a standart format)
- `blue_verified` (boolean, null): whether the account has the blue checkmark  
- `website` (text, null): personal or business website  
- `name` (text, not null): full name   
- `business_account` (boolean, null): if it's a business account  
- `owner` (text, null): the one who posted/shared (if reposted content)  
- `founder` (boolean, null): whether identified as a founder  
- `canadian` (boolean, null): whether located in Canada  
- `vc` (boolean, null): whether identified as a VC  
