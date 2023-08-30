#===================================================
# (1) COMPILED ANALYSIS - FB SCRAPING 
# AUGUST 2023
#===================================================
# core
from pathlib import Path
import pprint as pp
from tqdm import tqdm
import pandas as pd
import numpy as np
import requests
import json
from datetime import datetime
import time
import re

# fb scraper
from facebook_scraper import get_posts

# PATH TO JSON FACECBOOK COOKIES GO HERE
cookies_fb = ""

# initializing empty lists
raw_posts = []
posts = []

# columns
fields = ["user_id",
          "time",
          "post_text",
          "images_lowquality",
          "images_lowquality_description",
          "post_url"
         ]

# see functions.py for import statement
def post_to_df(post):
    df_raw = pd.DataFrame.from_dict(post, orient = "index").transpose()
    raw_posts.append(df_raw)
    
    df = df_raw[fields].copy()
    posts.append(df)

#----------------------------------------
# GRABBING POSTS
#----------------------------------------
options_dict = { "progress" : True }

print("RETRIEVING POSTS START: ",
      datetime.now().strftime("%x %-I:%M:%S %p"))

# comments on for debugging - comment out for quiet
[ (print("fetching post \n"),
   post_to_df(post),
   print("post df appended\n",
         "----------------------------------------------------------------------"),
   time.sleep(np.random.uniform(5.5, 12.5))
  ) for post in tqdm(get_posts(group = group_id, 
                          cookies = cookies_fb, 
                          pages = 55,
                          options = options_dict))
]

print("DONE RETRIEVING: ",
      datetime.now().strftime("%x %-I:%M:%S %p"))

# write to CSV
main_df = pd.concat(posts)
main_df.to_csv(dest, index=False)


### END OF FILE ###

