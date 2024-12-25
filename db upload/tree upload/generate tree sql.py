import pandas as pd
import numpy
import csv
import re
import bisect

def get_category_subcategory(df, index):
    cat = df.loc[index, "category"]; subcat = df.loc[index, "subcategory"]  # O( log(n) )
    return subcat, cat

def process_categories(df, start, end):
    queryList = []

    df_mapping = pd.read_excel("c:/Users/samia/OneDrive/Desktop/ISupply-project/db upload/Map upload/map.xlsx")  # load map
    category_mapping = sorted(df_mapping['combined'].items())  # make map dict(ionary) - sort it by key's
    category_mapping_keys = [k for k, v in category_mapping]  # extract keys
    
    for i in range(start, end):  # O(n*n)
        subcat, cat = get_category_subcategory(df, i); #num = str(num); cat = """ "Categories" """
        
        if(i % 100 == 0): print("map touched ", i)
        
        if (str(subcat) == "nan") and (str(type(subcat)) =="<class 'float'>"): subcat = '-1' # turn the nan into leafs before the mapping to prevent tree becoming a graph
        
        # binary search for cat & subcat
        cat_idx = bisect.bisect_left(category_mapping_keys, cat)
        if cat_idx < len(category_mapping_keys) and category_mapping_keys[cat_idx] == cat:
            cat = category_mapping[cat_idx][1]
        subcat_idx = bisect.bisect_left(category_mapping_keys, subcat)
        if subcat_idx < len(category_mapping_keys) and category_mapping_keys[subcat_idx] == subcat:
            subcat = category_mapping[subcat_idx][1]
        
                # print if n't strings
        if isinstance(cat, str) and cat != "-1":
            print(f"Non-string cat at index {i}: {cat} (type: {type(cat)})")
        if isinstance(subcat, str) and subcat != "-1":
            print(f"Non-string subcat at index {i}: {subcat} (type: {type(subcat)})")
        
        
        if (str(subcat) == "nan") and (str(type(subcat)) =="<class 'float'>"): query = f'INSERT INTO "Category_Tree" (category_id, sub_category_id) VALUES ({cat}, -1);' # leaf
        else: query = f'INSERT INTO "Category_Tree" (category_id, sub_category_id) VALUES (\'{cat}\', \'{subcat}\');' # non leaf
        queryList.append(query)

    print(len(queryList)); return queryList



def clean_line(line):
    line = line.replace("\\", "") # remove all backslashes
    def fix_quotes(value):
        if value.count("'") == 3:  # check if there are exactly three '
            parts = value.split("'")  # split by single quotes
            fixed_value = parts[0] + "'" + parts[1] + parts[2] + "');" # omit the second quote
            return f"{fixed_value};"  # return cleaned str w outer quotes
        return value
    
    return fix_quotes(line)

def modify_csv_lines(input_file, output_file):
    with open(input_file, 'r') as infile, open(output_file, 'w') as outfile:
        for line in infile:
            line = clean_line(line); line = line.strip()  # remove head whitespace
            if len(line) > 1: #safety case
                    # remove 1st, 14th, 26th, and -1st characters
                modified_line = ''.join(
                    char for i, char in enumerate(line)
                    if i not in {0, 13, 28, len(line) - 1}
                )
                outfile.write(modified_line + '\n')
            else:
                outfile.write(line + '\n')  # return unchanged if line is too short

df = pd.read_excel("c:/Users/samia/OneDrive/Desktop/ISupply-project/db upload/tree upload/slimTree.xlsx")# ; print(df.head())
df = df.drop_duplicates().reset_index()

queryList = []; queryList = process_categories(df, 0, 8415)# ; print(len(queryList))

# save as a CSV file
output_path = "c:/Users/samia/OneDrive/Desktop/ISupply-project/db upload/tree upload/query_list.csv"
query_df = pd.DataFrame(queryList); query_df.to_csv(output_path, index=False) # oop type shenanigans - to df & to csv

# run as a method for clean code reasons
input_csv = "C:/Users/samia/OneDrive/Desktop/ISupply-project/db upload/tree upload/query_list.csv"
output_csv = "C:/Users/samia/OneDrive/Desktop/ISupply-project/db upload/tree upload/query_list_clean.csv"
output_sql = "C:/Users/samia/OneDrive/Desktop/ISupply-project/db upload/tree upload/query_list_clean.sql"
modify_csv_lines(input_csv, output_csv)
modify_csv_lines(input_csv, output_sql)