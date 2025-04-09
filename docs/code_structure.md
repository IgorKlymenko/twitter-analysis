# General Code Structure  
## 3-step Pipeline  
- Extract Leads from followers/following of main — `get_leads.py`  
- Extract Posts from Leads until 6 months ago (or the last scraped post) — `get_posts.py`  
- Get Ranking / Filtering for all posts  

---

## Step-1: Extract Leads from followers/following  
- Receives a two-column `.csv` (without header) of `<name>, <twitter-profile-link>`  
- Processes all followers/following as a new set of leads and uploads to DB (**leads** table)  
- Params: you can change the upper limit of scraped followers/following (default is `"all"`)  

---

## Step-2: Extract Posts from Leads  
- Fetches the data from the DB (**leads** table) as input  
- Processes all Leads by scraping posts until 6 months from the current date or until it reaches an already scraped post, then uploads to DB (**posts** table)  
- Params: the oldest date to scrape posts until (default is 6 months)  

---

## Step-3: Get Ranking / Filtering  
- Fetches data from the DB (**posts** table) to analyze engagement, nationality (e.g., if Canadian), and profession (e.g., if founder, if VC)  
- Processes posts, location, descriptions, etc., and uploads scoring and analytics to DB (**final** table)  
- Params: no required params, but you can set up different metrics for scoring  