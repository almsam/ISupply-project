
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

* Converts string inputs into corresponding category IDs before processing
* Uses the absence of children in the tree to determine leaf status
