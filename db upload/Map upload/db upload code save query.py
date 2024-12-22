import pandas as pd
import numpy

df = pd.read_excel(
    "c:/Users/samia/OneDrive/Desktop/ISupply-project/db upload/Map upload/map.xlsx"
)
print(df.head())

def get_category_subcategory(df, index):
    num = df.loc[index, "Ser"]; name = df.loc[index, "combined"]  # O( log(n) )
    return name, num


def process_categories(df, start, end):
    queryList = []

    for i in range(start, end):  # O(n)
        name, num = get_category_subcategory(df, i); num = str(num); cat = """ "Categories" """
        query = f'INSERT INTO "Categories" (category_id, category) VALUES ({num}, \'{name}\');'
        queryList.append(query)

    print(len(queryList)); return queryList


queryList = []; queryList = process_categories(df, 0, 4596); print(len(queryList))


# save as a CSV file
output_path = "c:/Users/samia/OneDrive/Desktop/ISupply-project/db upload/Map upload/query_list.csv"
query_df = pd.DataFrame(queryList)  # oop type shenanigans
query_df.to_csv(output_path, index=False) 

print(f"Query list saved to {output_path}")

