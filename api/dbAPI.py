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
    id = map[map["cat"] == c] # change to an int
    if id.empty: raise ValueError(f"Node name '{c}' not found in 'Categories'.")
    return isLeafInt(id.iloc[0]["ser"]) #run int
def isLeafInt(id: int):
    if id == 0: raise ValueError(f"ID myst be non zero.") #start at 1
    if id == 1: return False #all is not a leaf
    children = tree[tree["cat"] == id]
    return children[children["subcat"] != -1].empty #a leaf is childless
def isLeaf(node) -> bool:
    if   isinstance(node, str): return isLeafStr(node) #str
    elif isinstance(node, int): return isLeafInt(node) #int
    else: raise TypeError("Node must be str or int")   #????

def getAllLeaves() -> list:
    leaves = []    # all nodes in the tree that are leaves
    for _, row in map.iterrows():  # for all categories
        category_id = row["ser"]
        if isLeaf(category_id): leaves.append(row["cat"])  # aff to the list
    return leaves

def isParentOfStr(subC: str, superC: str):
    sub_id = map[map["cat"] == subC]; super_id = map[map["cat"] == superC] #get ids
    if sub_id.empty: raise ValueError(f"Category name '{subC}' not found in 'Categories' ")
    if super_id.empty: raise ValueError(f"Category name '{superC}' not found in 'Categories' ")
    return isParentOfInt(sub_id.iloc[0]["ser"], super_id.iloc[0]["ser"])
def isParentOfInt(subId: int, superId: int):
    if subId == 0 or superId == 0: raise ValueError("IDs must be non zero")
    parent_row = tree[tree["subcat"] == subId]
    return not parent_row.empty and parent_row.iloc[0]["cat"] == superId #non empty & parentFound=parentGiven
def isParentOf(sub, super) -> bool:
    if isinstance(sub, str) and isinstance(super, str): return isParentOfStr(sub, super)
    elif isinstance(sub, str) and isinstance(super, str): return isParentOfStr(sub, super)
    else: raise TypeError("Both inputs must be str or both must be int")


map, tree = setup()

print("Leaves:", len(getAllLeaves()))
# print(isLeaf("Agricultural Equipment")); print(isLeaf("Agricultural Greenhouses")); print(isLeaf(99)); print(isLeaf(9)) #test for isLeaf