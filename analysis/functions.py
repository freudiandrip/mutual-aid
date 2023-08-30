################################################################################################
# extracting + cleaning functions - for scraped posts
# august 2023 - analysis: 
################################################################################################
# importing dependent libraries
import re
import regex
import pandas as pd

'''
NOTE: post_to_df is untested as an import function - paste into scraping script to run.
post_to_df(post)
    input: takes in a dictionary object
    output: none - appends a converted df from dict to empty pre-existing lists. 
'''
def post_to_df(post):
    df_raw = pd.DataFrame.from_dict(post, orient = "index").transpose()
    raw_posts.append(df_raw)
    
    df = df_raw[fields].copy()
    posts.append(df)


'''
extract(pattern, string, idx)
    input: takes in a re var pattern (str); post var string (str); and row index var idx(int)
    output: returns a match string or "none" string.
'''
def extract(pattern, string, idx):
    # re search
    m = re.search(pattern, string)
    
    #### debug mode #####
    # print("\n---------------------------------------------")
    # print(f"\ncurrently on row {idx}\n")
    # print("re.search results:\n", m)
    
    if m != None:
        match = m.group()
        
        #### DEBUG MODE #####
        # print("match found:\n")
        # print(match)
        
        return match

    elif m == None: 
        return "None"


'''
clean_asked(row, index)
    input: a pandas row dataframe; and row index var idx(int)
    output: returns a filterd amount int value  or "none" string.
'''
def clean_asked(row, idx):
    ########## DEBUG MODE ########################
    print("\n-----------------------------------------------------")
    print(f"\nON INDEX {idx}")
    asked = row["amount_asked"]
    
    # need to clean whitespace and symbols (,.$)
    symbols = "[\s\£\$\,\)\(\!\*]"
    m = re.sub(symbols, "", asked)
    
    if m != None:
        return float(m)
    
    else:
        return "None"


'''
clean_funded(row, idx)
    input: a pandas row dataframe; and row index var idx(int)
    output: returns a filtered float value  or "None" string.
'''
def clean_funded(row, idx):
    ### DEBUG MODE ###############
    print("\n---------------------------------------------------")
    print(f"\nCURRENTLY ON ROW {idx}\n")
    
    #extract the funded and asked amounts
    post_asked = row["amount_asked"]
    post_funded = row["amount_funded"]
    
    # cleaning
    symbols = "[\s\$\,\)\(\!\*\/]"
    asked = post_asked
    # asked = re.sub(symbols, "", post_asked)
    funded = re.sub(symbols, "", post_funded)

    # performing fund match for digit amount
    num_search = re.search("(\d+).{0,2}\d{0,2}", funded)

    # performing fund match for string fully funded
    fund_search = re.search(".*((?i)fund).*", funded)

    # CASE 1 + 2 - funding amount provided (without / with preceding text)
    if num_search != None:
        # print("Value provided:", num_search.group())
        symbols = "[^\d^\.]"
        m = re.sub(symbols, "", num_search.group())

        fund_amount = float(m)
        
        ### DEBUG MODE ###############
        print(f"Funding amount provided - funded for ${fund_amount}")
        
        return fund_amount

    # CASE 3 - funding amount not provided 
    elif num_search == None:
        # CASE 3A - request amount provided and fully funded
        if fund_search != None:
            fund_amount = float(asked)
            
            ### DEBUG MODE ###############
            print(f"Funding amount not provided - fully funded for ${fund_amount}")
            
            return fund_amount
        
        # CASE 3B - not fully funded but request amount provided
        elif fund_search != None and type(asked) == float:
            fund_amount = 0

            ### DEBUG MODE ###############
            print(f"Funding amount not provided - not funded")

            return fund_amount

        # CASE 3B - fully funded without amount context EMERGENCY CASE
        else:
            ### DEBUG MODE ###############
            print("Funding data (asked +  funded) not provided")
            
            return "None"




######## END OF FILE #########


