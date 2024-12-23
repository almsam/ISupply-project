import pandas as pd
import numpy
import csv
import re

def get_category_subcategory(df, index):
    cat = df.loc[index, "category"]; subcat = df.loc[index, "subcategory"]  # O( log(n) )
    return subcat, cat

def process_categories(df, start, end):
    queryList = []

    for i in range(start, end):  # O(n)
        subcat, cat = get_category_subcategory(df, i); #num = str(num); cat = """ "Categories" """
        query = f'INSERT INTO "Categories" (category_id, category) VALUES ({cat}, \'{subcat}\');'
        queryList.append(query)

    print(len(queryList)); return queryList


def modify_csv(input_file, output_file):
    with open(input_file, 'r') as infile, open(output_file, 'w', newline='') as outfile:
        reader = csv.reader(infile); writer = csv.writer(outfile)
        for row in reader:
            modified_row = []
            # for cell in row:
            #     if len(cell) > 1: #safety case
            #         # remove 1st, 14th, 26th, and -1st characters
            #         modified = ''.join(
            #             char for i, char in enumerate(cell); if i not in {len(cell)}#, 12, 25, len(cell) - 1}
            #         )
            #     else:
            #         modified = cell  # keep short strings unchanged
            #     modified_row.append(modified)
            # writer.writerow(modified_row)

def clean_line(line):
    line = line.replace("\\", "") # remove all backslashes
    def fix_quotes(value):
        if value.count("'") == 3:  # check if there are exactly three '
            parts = value.split("'")  # split by single quotes
            fixed_value = parts[0] + "'" + parts[1] + parts[2] + "');" # omit the second quote
            print(fixed_value); return f"{fixed_value};"  # return cleaned str w outer quotes
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
                    if i not in {0, 13, 25, len(line) - 1}
                )
                outfile.write(modified_line + '\n')
            else:
                outfile.write(line + '\n')  # return unchanged if line is too short

df = pd.read_excel("c:/Users/samia/OneDrive/Desktop/ISupply-project/db upload/tree upload/slimTree.xlsx")# ; print(df.head())

queryList = []; queryList = process_categories(df, 0, 13782)# ; print(len(queryList))

# save as a CSV file
output_path = "c:/Users/samia/OneDrive/Desktop/ISupply-project/db upload/tree upload/query_list.csv"
query_df = pd.DataFrame(queryList); query_df.to_csv(output_path, index=False) # oop type shenanigans - to df & to csv