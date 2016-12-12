# Author: Leslie Huang (lh1036)
# Description: Unit testing for the restaurantvisualizer methods
# I do not include unit tests for methods that only generate graphs

from inspectiongrades import RestaurantGrades
import unittest
import pandas as pd
import numpy as np
import numpy.testing as npt

class RestaurantGradesTestCase(unittest.TestCase):
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
            "inspectiondate": ["1/2/2014", "3/7/2012", "4/8/2016", "10/11/2015", "9/27/2014"],
            "zipcode": ["10011", "10003", "10011", "10024", "11211"]
        }
            
        dummy_restaurants = pd.DataFrame(data, columns = ["restaurant", "inspectiondate", "zipcode"])
        dummy_restaurants["inspectiondate"] = pd.to_datetime(dummy_restaurants["inspectiondate"], format = "%m/%d/%Y")
        self.dummy_data = dummy_restaurants.set_index("restaurant")

class RestaurantGradesTests(RestaurantGradesTestCase):
    '''
    Unit tests for methods from the RestaurantGrades class
    '''
    
    def test_filter_data(self):
        '''
        Test that filter_data returns DF subsetted by the requested zipcode
        '''
        test_data = {
            "restaurant": ["senor frog"],
            "inspectiondate": ["9/27/2014"],
            "zipcode": ["11211"]
        }
            
        test_restaurants = pd.DataFrame(test_data, columns = ["restaurant", "inspectiondate", "zipcode"])
        test_restaurants["inspectiondate"] = pd.to_datetime(test_restaurants["inspectiondate"], format = "%m/%d/%Y")
        
        test_restaurants = test_restaurants.set_index("restaurant")
        
        npt.assert_array_equal(
            RestaurantGrades("senor frog", self.dummy_data).filter_data(self.dummy_data),
            test_restaurants
        )
        
    