import unittest
import pandas as pd
from unittest.mock import patch
import psycopg2

from dbAPI import setup, isLeaf, getAllLeaves, isParentOf

class TestSetupFunction(unittest.TestCase):

    def test_setup_outputs(self):
        map, tree = setup() # call setup func
        
        # test output is df:
        self.assertIsInstance(map,  pd.DataFrame, "map is not a pd df")
        self.assertIsInstance(tree, pd.DataFrame, "tree is not a pd df")
        
        # test non empty:
        self.assertGreater(len(map),  0, "map df is empty")
        self.assertGreater(len(tree), 0, "tree df is empty")
        
        # verify columns:
        self.assertListEqual(list(map.columns),  ["ser", "cat"],          "map df columns incorrect")
        self.assertListEqual(list(tree.columns), ["id", "cat", "subcat"], "tree df columns incorrect")

    def test_isLeaf(self):
        self.assertFalse(isLeaf("Agricultural Equipment"))
        self.assertTrue(isLeaf("Agricultural Greenhouses"))
        
        self.assertFalse(isLeaf(99))
        self.assertTrue(isLeaf(9))
        
        self.assertFalse(isLeaf(1))
        self.assertFalse(isLeaf("all"))
        
        with self.assertRaises(ValueError) as context: isLeaf(0)
        self.assertIn("ID myst be non zero.", str(context.exception))

    def test_getAllLeaves(self):
        self.assertEqual(len(getAllLeaves()), 3536)

    def test_isParentof(self):
        self.assertTrue(isParentOf(2, 1)) #all
        self.assertTrue(isParentOf(3, 2)) #norm true
        self.assertFalse(isParentOf(2, 3)) #reverse norm true
        self.assertFalse(isParentOf(19, 12)) #norm false

if __name__ == "__main__":
    unittest.main()
