# Author: Leslie Huang (lh1036)
# Description: Unit testing for the Visualizer superclass methods
# I do not include trivial tests for methods that implement a simple Pandas operation
# e.g. group_by_sidewalk()

from inspectiongrades.visualizer import Visualizer
import unittest
import pandas as pd
import numpy as np
import numpy.testing as npt

class VisualizerTestCase(unittest.TestCase):
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
            "cuisine_primary": ["thai", "pizza", "sandwiches", "french", "sandwiches"],
            "restaurant": ["thai garden", "'za for days", "sandwich world", "onion soup waterpark", "senor frog"],
            "boro": ["manhattan", "brooklyn", "missing", "bronx", "queens"],
            "swc_type": ["no cafe", "no cafe", "regular unenclosed", "enclosed", "small enclosed"],
            "score": [0, 100, 10, 57, 23],
            "grade": ["a", "c", "a", "grade pending", "b"],
            "inspectiondate": ["1/2/2014", "3/7/2012", "4/8/2016", "10/11/2015", "9/27/2014"]
                }
            
        dummy_restaurants = pd.DataFrame(data, columns = ["cuisine_primary", "restaurant", "boro", "swc_type", "score", "grade", "inspectiondate"])
        dummy_restaurants["inspectiondate"] = pd.to_datetime(dummy_restaurants["inspectiondate"], format = "%m/%d/%Y")
        self.dummy_data = dummy_restaurants.set_index("restaurant")


class VisualizerTests(VisualizerTestCase):
    '''
    Unit tests for methods from the Visualizer class
    '''
    
    def test_filter_data_valid_values(self):
        '''
        Test that filter_data_valid_values returns DataFrame with obs filtered correctly
        '''
        
        # set up a result DataFrame for comparison
        test_data = {
            "cuisine_primary": ["thai"],
            "restaurant": ["thai garden"],
            "boro": ["manhattan"],
            "swc_type": ["no cafe"],
            "score": [0],
            "grade": ["a"],
            "inspectiondate": ["1/2/2014"]
                }
                
        test_restaurant = pd.DataFrame(test_data, columns = ["cuisine_primary", "restaurant", "boro", "swc_type", "score", "grade", "inspectiondate"])
        test_restaurant["inspectiondate"] = pd.to_datetime(test_restaurant["inspectiondate"], format = "%m/%d/%Y")
        test_restaurant = test_restaurant.set_index("restaurant")
        
        npt.assert_array_equal(Visualizer(self.dummy_data).filter_data_valid_values("boro", ["manhattan"]), test_data)

    def test_calculate_mean_by_restaurant(self):
        '''
        Test that calculate_mean_by_restaurant returns mean inspection scores by restaurant
        '''
        npt.assert_array_equal(Visualizer(self.dummy_data).calculate_mean_by_restaurant(), [[0], [10], [23], [57], [100]])
    
    def test_get_best_and_worst_names(self):
        '''
        Test that the method returns a list of the best and worst restaurant names
        '''
        self.assertEqual(Visualizer(self.dummy_data).get_best_and_worst_names(1), ["thai garden", "'za for days"])

    def test_group_scores_by_category(self):
        '''
        Test that group_scores_by_category returns a sorted and grouped DF of mean scores by cuisine
        '''
        # Set up result DF for comparison
        test_data = {
            "cuisine_primary": ["thai", "pizza", "sandwiches", "french"],
            "restaurant": ["thai garden", "'za for days", "sandwich world", "onion soup waterpark"],
            "score": [0., 100., 16.5, 57.],
                }
        test_restaurants = pd.DataFrame(test_data, columns = ["cuisine_primary", "score"])
        test_restaurants = test_restaurants.set_index(["cuisine_primary"])
        
        npt.assert_array_equal(Visualizer(self.dummy_data).group_scores_by_category(), test_restaurants.sort_values(by = "score"))

class GetBestAndWorstDataTests(VisualizerTestCase):
    '''
    Check that get_best_and_worst_data returns the DataFrames of the best and worst restaurants
    Note: To check for equality of a tuple (DataFrame, DataFrame), I unpack and check each DataFrame individually
    '''
    
    def test_get_best_data(self):
        '''
        Test that the function correctly returns the observations of the best restaurant 
        '''
        # Set up the result DataFrame for comparison
        best_data = {
            "cuisine_primary": ["thai"],
            "restaurant": ["thai garden"],
            "boro": ["manhattan"],
            "swc_type": ["no cafe"],
            "score": [0],
            "grade": ["a"],
            "inspectiondate": ["1/2/2014"]
                }
        best_restaurant = pd.DataFrame(best_data, columns = ["cuisine_primary", "restaurant", "boro", "swc_type", "score", "grade", "inspectiondate"])
        best_restaurant["inspectiondate"] = pd.to_datetime(best_restaurant["inspectiondate"], format = "%m/%d/%Y")
        best_restaurant = best_restaurant.set_index("restaurant")
        
        npt.assert_array_equal(Visualizer(self.dummy_data).get_best_and_worst_data(1)[0], best_restaurant)
        
    def test_get_worst_data(self):
        '''
        Test that the function correctly returns the observations of the worst restaurant 
        '''
        
        # Set up the result DataFrame for comparison
        worst_data = {
            "cuisine_primary": ["pizza"],
            "restaurant": ["'za for days"],
            "boro": ["brooklyn"],
            "swc_type": ["no cafe"],
            "score": [100],
            "grade": ["c"],
            "inspectiondate": ["3/7/2012"]
                }
        worst_restaurant = pd.DataFrame(worst_data, columns = ["cuisine_primary", "restaurant", "boro", "swc_type", "score", "grade", "inspectiondate"])
        worst_restaurant["inspectiondate"] = pd.to_datetime(worst_restaurant["inspectiondate"], format = "%m/%d/%Y")
        worst_restaurant = worst_restaurant.set_index("restaurant")
        
        npt.assert_array_equal(Visualizer(self.dummy_data).get_best_and_worst_data(1)[1], worst_restaurant)
        

if __name__ == "__main__":
    unittest.main()
    