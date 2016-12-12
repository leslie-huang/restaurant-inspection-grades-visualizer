# Author: Leslie Huang (lh1036)
# Description: Unit testing for the zipvisualizer methods
# I do not include unit tests for methods that only generate graphs

from inspectiongrades import ZipGrades
import unittest
import pandas as pd
import numpy as np
import numpy.testing as npt

class ZipGradesTestCase(unittest.TestCase):
    '''
    Base class for unittesting functions that require a restaurant_data dataset
    '''
    
    def setUp(self):
        '''
        Create a dummy dataset for testing
        Note: In the cleaned dataset, all strings are lowercased for case-insensitive 
        matching to user input. I preserve the same convention here.
        '''
        data = {
            "restaurant": ["thai garden", "'za for days", "sandwich world", "onion soup waterpark", "senor frog"],
            "zipcode": ["10011", "10003", "10011", "10024", "11211"]
        }
            
        dummy_restaurants = pd.DataFrame(data, columns = ["restaurant", "zipcode"])
        self.dummy_data = dummy_restaurants.set_index("restaurant")

class ZipGradesTests(ZipGradesTestCase):
    '''
    Unit tests for methods from the ZipGrades class
    '''
    
    def test_filter_data(self):
        '''
        Test that filter_data returns DF subsetted by the requested zipcode
        '''
        test_data = {
            "restaurant": ["senor frog"],
            "zipcode": ["11211"]
        }
            
        test_restaurants = pd.DataFrame(test_data, columns = ["restaurant", "zipcode"])
        test_restaurants = test_restaurants.set_index("restaurant")
        
        npt.assert_array_equal(ZipGrades("11211", self.dummy_data).filter_data(self.dummy_data), test_restaurants)
        
    