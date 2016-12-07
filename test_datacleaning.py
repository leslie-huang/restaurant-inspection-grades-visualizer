# Tests for the datacleaning helper functions in datacleaning.py

import unittest
from datacleaning import *
import pandas as pd
import numpy.testing as npt

class RestaurantTestCase(unittest.TestCase):
    '''
    Base class for unittesting functions that require a dataset (which is all of them)
    '''
    
    def setUp(self):
        '''
        Create a dummy dataset for testing
        '''
        data = {
            "NAME": ["Olive Garden", "Pizza Farm", "Sandwich WORLD", "Soup Waterpark", ""],
            "BUILDING": ["", 123, 4, 5, 6],
            "STREET": ["West 4th", "", "West 3rd", "Bleecker", "Broadway"],
            "CUISINE DESCRIPTION": ["Italian/Pizza", "Pizza", "Sandwiches, bread, stuff", "Soup, water", "Bananas"]
            }
        dummy_restaurants = pd.DataFrame(data, dtype = str)
        self.dummy_data = dummy_restaurants


class DataCleaningTests(RestaurantTestCase):
    
    def test_clean_colnames(self):
        '''
        Check that function correctly lowercasing and removing white space from col names
        '''
        
        npt.assert_array_equal(clean_colnames(self.dummy_data.columns, pd.Index(["name", "building", "street", "cuisine description"]))
        
    
if __name__ == "__main__":        
    unittest.main()
    
        