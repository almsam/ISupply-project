import pandas as pd
import psycopg2
import numpy as np

def setup():
    con = psycopg2.connect(
        database="iSupply",
        host="38.180.117.52",
        user="postgres",
        password="deerRun",
        port="5432",
    )
    cursor = con.cursor() #open
    cursor.execute("""select * from "Categories" c""")   ; outMap  = cursor.fetchall()  # make a dictionary of what the db currently has
    cursor.execute("""select * from "Category_Tree" c"""); outTree = cursor.fetchall()  # repeat for tree
    cursor.close(); con.close() # n close

    map = pd.DataFrame(outMap, columns=["ser", "cat"]); print(map)
    tree = pd.DataFrame(outTree, columns=["id", "cat", "subcat"]); print(tree); return map, tree

#main:


def isLeaf(c: str):
    id = map[map["cat"] == c]
    if id.empty: raise ValueError(f"Node name '{c}' not found in 'Categories'.")
    return isLeaf(id.iloc[0]["ser"])

def isLeaf(id: int):
    children = tree[tree["id"] == id]
    return children.empty

map, tree = setup()

print(isLeaf(10))