import pandas as pd
import numpy
import csv
import re
import bisect

def get_category_subcategory(df, index):
    cat = df.loc[index, "category"]; subcat = df.loc[index, "subcategory"]  # O( log(n) )
    return subcat, cat

def process_categories(df, start, end):
    queryList = []; non_int_cats = []; non_int_subcats = []

    df_mapping = pd.read_csv("c:/Users/samia/OneDrive/Desktop/ISupply-project/db upload/tree upload/liveMap.csv")  # load map
    df_mapping = df_mapping.replace({"'": "", r"\\": "", r"//": "", r"/": ""}, regex=True)
    category_mapping = sorted([(str(k), v) for k, v in zip(df_mapping['cat'], df_mapping['ser'])])  # make map dict(ionary) - sort it by key's
    category_mapping_keys = [k for k, v in category_mapping]  # extract keys
    
    for i in range(start, end):  # O(n*n)
        subcat, cat = get_category_subcategory(df, i); #num = str(num); cat = """ "Categories" """
        
        if(i % 100 == 0): print("map touched ", i)
        
        if (str(subcat) == "nan") and (str(type(subcat)) =="<class 'float'>"): subcat = '-1' # turn the nan into leafs before the mapping to prevent tree becoming a graph
        
        cat = str(cat).replace("'", "").replace("\\", "").replace("//", "").replace("/", "")
        subcat = str(subcat).replace("'", "").replace("\\", "").replace("//", "").replace("/", "")
        
        # binary search for cat & subcat
        cat_idx = bisect.bisect_left(category_mapping_keys, str(cat))
        if cat_idx < len(category_mapping_keys) and category_mapping_keys[cat_idx] == cat:
            cat = category_mapping[cat_idx][1]
        subcat_idx = bisect.bisect_left(category_mapping_keys, str(subcat))
        if subcat_idx < len(category_mapping_keys) and category_mapping_keys[subcat_idx] == subcat:
            subcat = category_mapping[subcat_idx][1]
        
                # print if strings &n't ints
        if isinstance(cat, str) and cat != "-1":
            non_int_cats.append((cat)) # print(f"Non-int cat at index {i}: {cat} (type: {type(cat)})")
        if isinstance(subcat, str) and subcat != "-1":
            non_int_subcats.append((subcat)) # print(f"Non-int subcat at index {i}: {subcat} (type: {type(subcat)})")
        
        
        if (str(subcat) == "nan") and (str(type(subcat)) =="<class 'float'>"): query = f'INSERT INTO "Category_Tree" (category_id, sub_category_id) VALUES ({cat}, -1);' # leaf
        else: query = f'INSERT INTO "Category_Tree" (category_id, sub_category_id) VALUES (\'{cat}\', \'{subcat}\');' # non leaf
        queryList.append(query)
    
    print("\n\n\n\n\n ERROR LIST: \n\n\n")
    non_int_cats = list(set(non_int_cats)); non_int_subcats = list(set(non_int_subcats))
    print("Non-integer cat's:")
    for value in non_int_cats: print(f"value: {value}")
    print("Non-integer subcat's:")
    for value in non_int_subcats: print(f"value: {value}")
    
    #save
    with open("non_int_cats.csv",    "w", newline="", encoding="utf-8") as file: writer = csv.writer(file); writer.writerows([[item] for item in non_int_cats   ])
    with open("non_int_subcats.csv", "w", newline="", encoding="utf-8") as file: writer = csv.writer(file); writer.writerows([[item] for item in non_int_subcats])
    
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