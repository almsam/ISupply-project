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


def isLeafStr(c: str):
    id = map[map["cat"] == c]
    if id.empty: raise ValueError(f"Node name '{c}' not found in 'Categories'.")
    return isLeafInt(id.iloc[0]["ser"])

def isLeafInt(id: int):
    if id == 0: raise ValueError(f"ID myst be non zero.")
    if id == 1: return False
    children = tree[tree["cat"] == id]
    return children[children["subcat"] != -1].empty

def isLeaf(node) -> bool:
    if isinstance(node, str): isLeafStr(node)
    elif isinstance(node, int): isLeafInt(node)
    else:
        raise TypeError("Node must be str or int")


map, tree = setup()


