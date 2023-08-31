#===================================================
# (2) COMPILED ANALYSIS - FLOAT EXTRACTION 
# AUGUST 2023
#===================================================
# core
from pathlib import Path
import pprint as pp
from tqdm import tqdm
import pandas as pd
import numpy as np
import re
import regex

# FB post functions
from functions import extract
from functions import clean_asked
from functions import clean_funded

# read in CSVs 
read_path = Path("PATH/TO/CSV/HERE.csv")

# working dataframes
df_raw = pd.read_csv(read_path)
wip = df_raw.copy()
amount_df = wip[["post_id", "post_text"]]

#----------------------------------------
# extracting amount requested
#----------------------------------------
ask_pattern = "(?<=\/)\s*(\$?|\£?)\s*\d+(\,?)\d*(\.?)\d*(?=.*\n)"

# extracting request values
amount_df["amount_asked"] = (
    amount_df["post_text"].apply(
        lambda x: extract(ask_pattern,
                          x,
                          amount_df[amount_df['post_text'] == x].index))
)


#----------------------------------------
# extracting amount funded
#----------------------------------------
fund_pattern = ".*((?i)full)?.*((?i)fund)?.*\d*(?=\s*\/\s*(\$?|\£?)\s*\d+.*\n)"

# extracting funded values
amount_df["amount_funded"] = (
    amount_df["post_text"].apply(
        lambda x: extract(fund_pattern,
                          x, 
                          amount_df[amount_df['post_text'] == x].index))
)


#----------------------------------------
# cleaning values --> converting to floats 
#----------------------------------------
# cleaning extracted requested values
amount_df["amount_asked"] = (
    amount_df.apply(lambda row: clean_asked(row, row.name), axis=1)
)

# cleaning extracted funded values
amount_df["amount_funded"] = (
    amount_df.apply(lambda row: clean_funded(row, row.name), axis=1)
)

wip_df.to_csv(wip_path, index=False)

### END OF FILE ###

