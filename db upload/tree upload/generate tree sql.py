import pandas as pd
import numpy
import csv
import re

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