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
    if parent_row.empty and superId == 1: return True #all case
    return not parent_row.empty and parent_row.iloc[0]["cat"] == superId #non empty & parentFound=parentGiven
def isParentOf(sub, super) -> bool:
    if isinstance(sub, str) and isinstance(super, str): return isParentOfStr(sub, super)
    elif isinstance(sub, int) and isinstance(super, int): return isParentOfInt(sub, super)
    else: raise TypeError("Both inputs must be str or both must be int")

def findParentOfStr(sub: str) -> tuple:
    sub_id = map[map["cat"] == sub]
    if sub_id.empty: raise ValueError(f"Node name '{sub}' not found in 'Categories' ")
    sub_id = sub_id.iloc[0]["ser"]; return findParentOfInt(sub_id)
def findParentOfInt(sub_id: int) -> tuple:
    if sub_id == 0: raise ValueError("ID must be non-zero")
    if sub_id == 1: return (1, "all") #all is parent of all

    parent_row = tree[tree["subcat"] == sub_id] # find parent
    if parent_row.empty: return (1, "all")

    parent_id = parent_row.iloc[0]["cat"]; parent_name = map[map["ser"] == parent_id]["cat"].iloc[0]
    return (parent_id, parent_name) # return ID & name
def findParentOf(sub) -> tuple:
    if isinstance(sub, str): return findParentOfStr(sub)
    elif isinstance(sub, int): return findParentOfInt(sub)
    else: raise TypeError("Input must be of type str or int")

def findChildrenOfStr(super: str) -> list:
    super_id = map[map["cat"] == super] #to int
    if super_id.empty: raise ValueError(f"Category name '{super}' not found in 'Categories'") # if invalid
    return findChildrenOfInt(super_id.iloc[0]["ser"]) # run int side
def findChildrenOfInt(super_id: int) -> list:
    if super_id == 0: raise ValueError("ID must be non-zero")
    children_rows = tree[tree["cat"] == super_id] # get rows where `cat` matches `super_id`
    children = []
    for _, row in children_rows.iterrows(): # extract IDs & their names
        child_id = row["subcat"]
        if child_id != -1:  # checks for invalid kids
            child_name = map[map["ser"] == child_id]["cat"].iloc[0]; children.append((child_id, child_name))
    return children
def findChildrenOf(super) -> list:
    if isinstance(super, str): return findChildrenOfStr(super)
    elif isinstance(super, int): return findChildrenOfInt(super)
    else: raise TypeError("Input must be of type str or int")


map, tree = setup()

# print(findParentOf(1)) print(findParentOf(2)) print(findParentOf(3)) print(findParentOf(4)) print(findParentOf(12))
# print(isParentOf(2, 1)) #all        print(isParentOf(3, 2)) #norm true      print(isParentOf(2, 3)) #reverse norm true      print(isParentOf(19, 12)) #norm false
# print("Leaves:", len(getAllLeaves()))
# print(isLeaf("Agricultural Equipment")); print(isLeaf("Agricultural Greenhouses")); print(isLeaf(99)); print(isLeaf(9)) #test for isLeaf