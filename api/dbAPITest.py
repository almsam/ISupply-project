import unittest
import pandas as pd
from unittest.mock import patch
import psycopg2

from dbAPI import setup, isLeaf

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
        map, tree = setup() # call setup func
        

if __name__ == "__main__":
    unittest.main()
