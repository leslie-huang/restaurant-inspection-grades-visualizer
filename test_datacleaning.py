# Tests for the datacleaning helper functions in datacleaning.py

import unittest
from datacleaning import *
import pandas as pd
import numpy.testing as npt
import numpy as np

class RestaurantTestCase(unittest.TestCase):
    '''
    Base class for unittesting functions that require a dataset (which is all of them)
    '''
    
    def setUp(self):
        '''
        Create a dummy dataset for testing
        '''
        data = {
            "BUILDING": ["200", "123", "4", "5", "6"],
            "CUISINE DESCRIPTION": ["Italian/Pizza", "Pizza", "Sandwiches, bread, stuff", "Soup, water", ""],
            "NAME": ["Olive  Garden", "Pizza Farm", "Sandwich WORLD  ", "Soup Waterpark", ""],
            "STREET": ["West  4th", "", "West  3rd", "Bleecker", "Broadway"],
            }
        dummy_restaurants = pd.DataFrame(data, dtype = str, columns = ["BUILDING", "CUISINE DESCRIPTION", "NAME", "STREET"])
        self.dummy_data = dummy_restaurants


class DataCleaningTests(RestaurantTestCase):
    
    def test_clean_colnames(self):
        '''
        Check that function correctly lowercases and removes white space from col names
        '''
        npt.assert_array_equal(
        clean_colnames(self.dummy_data).columns, 
        pd.Index(["building", "cuisinedescription", "name", "street"])
        )
    
    def test_convert_lowercase(self):
        '''
        Check that all function lowercases DF
        '''
        npt.assert_array_equal(
        convert_lowercase(self.dummy_data).iloc[2], 
        pd.Series({"NAME": "sandwich world  ", "BUILDING": "4", "STREET": "west  3rd", "CUISINE DESCRIPTION": "sandwiches, bread, stuff"})
        )
    
    def test_strip_whitespace(self):
        '''
        Check that strip_whitespace removes excess whitespace from specified columns
        '''
        npt.assert_array_equal(
        strip_whitespace(self.dummy_data, ["NAME", "STREET"]).iloc[2], 
        pd.Series({"NAME": "Sandwich WORLD", "BUILDING": "4", "STREET": "West 3rd", "CUISINE DESCRIPTION": "Sandwiches, bread, stuff"})
        )
    
    def test_concat_cols(self):
        '''
        Check that concat_cols creates a new column concatenated from specified existing columns
        '''
        npt.assert_array_equal(
            concat_cols(self.dummy_data, ["BUILDING", "STREET"], "address")["address"],
            pd.Series({0: "200 West  4th", 1: "123 ", 2: "4 West  3rd", 3: "5 Bleecker", 4: "6 Broadway"})
        )
        
    
    def test_make_primary_cuisine(self):
        '''
        Check that make_primary_cuisine creates a new column of the first listed cuisine
        '''
        npt.assert_array_equal(
            make_primary_cuisine(self.dummy_data, "CUISINE DESCRIPTION", "primary")["primary"],
            pd.Series({0: "Italian", 1: "Pizza", 2: "Sandwiches", 3: "Soup", 4: ""})
        )
   
    def test_drop_multiple_column_nulls(self):
        '''
        Check that function drops all observations with any nulls in specified cols
        '''
        npt.assert_array_equal(
            drop_multiple_column_nulls(self.dummy_data, ["CUISINE DESCRIPTION", "NAME", "STREET"]),
            pd.DataFrame(
                {
                    "BUILDING": ["200", "4", "5"], 
                    "CUISINE DESCRIPTION": ["Italian/Pizza", "Sandwiches, bread, stuff", "Soup, water"], 
                    "NAME": ["Olive  Garden", "Sandwich WORLD  ", "Soup Waterpark"], 
                    "STREET": ["West  4th", "West  3rd", "Bleecker"]
                },
                dtype = str
            )
        )

if __name__ == "__main__":        
    unittest.main()
    
        