
# Documentation for Our API

This document explains the purpose and functionality of the key methods provided in the code for working with the API for the Database. The methods facilitate determining relationships, navigating through parent-child structures, and retrieving hierarchical data from our database.

---

## 1. `isLeaf(Node)`

### **Purpose**

Determines whether a given node is a leaf node (i.e., has no children)

### **Parameters**

* `node` (*str* or *int*): The category name (*str*) or category ID (*int*)

### **Returns**

* (*bool*): if the node is a leaf, otherwise

### **Behavior**

* O(n)
* Converts string inputs into corresponding category IDs before processing
* Uses the absence of children in the tree to determine leaf status

---

## 2. `getAllLeaves()`

### **Purpose**

Retrieves a list of all categories in the tree that are leaves.

### **Parameters**

None.

### **Returns**

* (*list[str]*): A list of category names that are leaves.

### **Key Behavior**

* Iterates through all categories O(n^2)
* Uses the `isLeaf()` method to check each

---

## 3. `isParentOf(superNode, subNode)`

### **Purpose**

Checks if one category is the parent of another

### **Parameters**

* `sub` (*str* or *int*): The child category name (*str*) or ID (*int*)
* `super` (*str* or *int*): The parent category name (*str*) or ID (*int*)

### **Returns**

* (*bool*): `True` if `super` is the parent of `sub`, otherwise `False`

### **Key Behavior**

* O(n)
* Allows checking parent-child relationships directly via IDs in the `Category_Tree` dataframe

---

## 4. `findParentOf(Node)`

### **Purpose**

Finds the immediate parent of a given category

### **Parameters**

* `Node` (*str* or *int*): The category name (*str*) or ID (*int*)

### **Returns**

* `(*tuple[int, str]*)`: A tuple containing the parent category ID and name

### **Key Behavior**

* Returns the parent of "all" as itself
* Uses the `Category_Tree` dataframe to find paren
* Handles cases where a category has no parent by returning self's root
* O(n)

---

## 5. `findChildrenOf(Node)`

### **Purpose**

Finds all immediate children of a given category

### **Parameters**

* `Node` (*str* or *int*): The parent category name (*str*) or ID (*int*)

### **Returns**

* `(*list[tuple[int, str]]*)`: A list of tuples, where each tuple contains the child category ID and name.

### **Key Behavior**

* For the root category - "all" - returns categories with no parents
* Uses the `Category_Tree` dataframe to retrieve child nodes
* Filters out invalid children (e.g., `-1`)
* O(n)

---

