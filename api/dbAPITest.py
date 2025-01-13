import unittest
import pandas as pd
from unittest.mock import patch
import psycopg2

from dbAPI import setup, isLeaf, getAllLeaves, isParentOf, findParentOf, findChildrenOf, getAllCategories, getRoot

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

    def test_findParentof(self):
        self.assertEqual((findParentOf(1)),  (1, 'all'))
        self.assertEqual((findParentOf(2)),  (1, 'all'))
        self.assertEqual((findParentOf(3)),  (2, 'Agriculture'))
        self.assertEqual((findParentOf(4)),  (3, 'Agricultural Equipment'))
        self.assertEqual((findParentOf(12)), (2, 'Agriculture'))

    def test_findChildrenof(self):
        self.assertListEqual(
            findChildrenOf("Agricultural Equipment"),
            [(4, 'Agricultural Greenhouses'), (5, 'Aquaculture Equipment'), (11, 'Ear Tag')], "str failed"
        )
        self.assertListEqual(
            findChildrenOf(3),
            [(4, 'Agricultural Greenhouses'), (5, 'Aquaculture Equipment'), (11, 'Ear Tag')], "int failed"
        )
        
        self.assertListEqual(
            findChildrenOf("Agricultural Greenhouses"),
            [], "clildless case failed"
        )
        
        self.assertGreater(len(findChildrenOf("all")), 0, "'all' category should have children")
        
        # test invalid str, int, type
        
        with self.assertRaises(ValueError) as context:
            findChildrenOf("Nonexistent Category")
        self.assertIn("Category name 'Nonexistent Category' not found", str(context.exception))
        
        with self.assertRaises(ValueError) as context:
            findChildrenOf(0)
        self.assertIn("ID must be non-zero", str(context.exception))
        
        with self.assertRaises(TypeError) as context:
            findChildrenOf(2.5)  # Invalid type (float)
        self.assertIn("Input must be of type str or int", str(context.exception))

    def test_getAllCategories(self):
        expected = [(1, 'all'), (2, 'Agriculture'), (153, 'Apparel'), (342, 'Automobiles & Motorcycle s'), (536, 'Beauty & Personal Care'), (750, 'Business Services'), (833, 'Computer & Information Technology Consulting'), (877, 'Measuring & Analysing Instrument Pr ocessing Services'), (928, 'Chemicals'), (1012, 'Computer Hardware & So ftware'), (1071, 'Construction & Real Estat e'), (1317, 'Consumer Electronics'), (1385, 'Electrical Equipment & Su pplies'), (1468, 'Electronic Components & Supplies'), (1512, 'Energy'), (1546, 'Environment'), (1561, 'Excess Inventory'), (1567, 'Fashion Accessories'), (1646, 'Food & Beverage'), (1816, 'Furniture'), (1951, 'Gifts & Crafts'), (1995, 'Hardware'), (2018, 'Health & Medical'), (2075, 'Home & Garden'), (2345, 'Home Appliances'), (2514, 'Lights & Lighting'), (2581, 'Luggage, Bags & Cases'), (2634, 'Machinery'), (2978, 'Used Machinery & Equipment Auctio n Service'), (3040, 'Measurement & Analysis I nstruments'), (3076, 'Measuring & Analysing Instrument Desi gn Services'), (3077, 'Measuring & Analysing Instrument Proc essing Services'), (3122, 'Mechanical Parts & Fabric ation Services'), (3208, 'Minerals & Metallurgy'), (3389, 'Office & School Supplies'), (3550, 'Packaging & Printing'), (3605, 'Rubber & Plastics'), (3681, 'Security & Protection'), (3765, 'Service Equipment'), (3820, 'Shoes & Accessories'), (3873, 'Sports & Entertainment'), (4071, 'Telecommunications'), (4123, 'Textiles & Leather Produc ts'), (4261, 'Timepieces, Jewelry, Eyew ear'), (4317, 'Tools'), (4407, 'Toys & Hobbies'), (4477, 'Transportation x x')]
        self.assertEqual(getAllCategories(), expected, "The getAllCategories method does not seem correct")

    def test_getRoot(self):
        
        # categories get a test each
        
        self.assertEqual(
            getRoot("Agricultural Greenhouses"),
            [(1, "all"), (2, "Agriculture"), (3, "Agricultural Equipment")],
            "Failed to correctly get hierarchy for 'Agricultural Greenhouses'"
        )
        
        self.assertEqual(
            getRoot("Kidney Beans"),
            [(1, "all"), (2, "Agriculture"), (26, "Beans")],
            "Failed to correctly trace hierarchy for 'Farming' "
        )
        
        self.assertEqual(
            getRoot(4),
            [(1, "all"), (2, "Agriculture"), (3, "Agricultural Equipment")],
            "Failed to correctly trace hierarchy for cat ID 4"
        )
        
        self.assertEqual(
            getRoot(2),
            [(1, "all")],
            "Failed to correctly trace hierarchy for the prime category (child of'all')"
        )
        
        self.assertEqual(
            getRoot(1),
            [],
            "Failed to correctly trace hierarchy for all"
        )



if __name__ == "__main__":
    unittest.main()
