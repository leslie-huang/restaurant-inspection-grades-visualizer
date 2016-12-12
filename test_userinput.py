# Author: Leslie Huang (lh1036)
# Description: unit tests for helper functions that handle and parse user input

import unittest
from userinput import *
from exceptions import *
import pandas as pd

class QuittingInputTests(unittest.TestCase):
    '''
    Test that quitting_input ends program when input is "finish" but not otherwise
    '''
    
    def test_finish(self):
        '''
        Tests that QuitError is correctly raised when the user inputs 'finish'
        '''
        with self.assertRaises(QuitError):
            quitting_input("", lambda _: "finish")
            
    def test_valid_cuisine(self):
        '''
        Test that quitting_input returns the user's input if not 'finish' 
        (passes input to the next function)
        '''
        self.assertEqual(quitting_input("", lambda _: "Pizza"), "Pizza")

class RestaurantDataTestCase(unittest.TestCase):
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
            "zipcode": ["10011", "11211", "10002", "12345", "54321"],
            "cuisine_primary": ["thai", "pizza", "sandwiches", "french", "sandwiches"],
            "restaurant": ["thai garden", "'za for days", "sandwich world", "onion soup waterpark", "senor frog"]
                }
            
        dummy_restaurants = pd.DataFrame(data, columns = ["zipcode", "cuisine_primary", "restaurant"])
        self.dummy_data = dummy_restaurants.set_index("restaurant")


### Unit testing of the validate functions for cuisine, restaurant, and zipcode

class ValidateCuisineTests(RestaurantDataTestCase):
    '''
    Test that validate_cuisine returns lowercased str of cuisine if in dataset,
    or raises custom error if not
    '''
    def test_valid_cuisine(self):
        '''
        Test that function validates a cuisine in the dataset
        '''
        self.assertEqual(validate_cuisine("Pizza", self.dummy_data), "pizza")
    
    def test_invalid_cuisine(self):
        '''
        Tests that custom exception is raised with cuisine not in dataset
        '''
        with self.assertRaises(InvalidCuisineError):
            validate_cuisine("japanese", self.dummy_data)

class ValidateRestaurantNameTests(RestaurantDataTestCase):
    '''
    Tests that validate_restaurant_name returns lowercased str
    of restaurant name if in dataset, or raise an exception if not
    '''
    def test_valid_restaurant(self):
        '''
        Test that function validates a restaurant in the dataset
        '''
        self.assertEqual(validate_restaurant_name("SANDWICH world", self.dummy_data, 0), "sandwich world")
        
    def test_invalid_restaurant(self):
        '''
        Test that an invalid name raises exception
        '''
        with self.assertRaises(InvalidRestaurantNameError):
            validate_restaurant_name("soup aquarium", self.dummy_data, 0)
            
class ValidateZipTests(RestaurantDataTestCase):
    '''
    Tests that validate_zip returns zipcode as int
    if in dataset, or raise an exception if not
    '''
    def test_valid_zip(self):
        '''
        Test that function returns zipcode as int when validated
        '''
        self.assertEqual(validate_zip("11211", self.dummy_data), "11211")
    
    def test_invalid_zip(self):
        '''
        Test that function raises exception when invalid zip is entered
        '''
        with self.assertRaises(InvalidZipError):
            validate_zip("foo", self.dummy_data)

### Unit testing of the prompt functions for cuisine, restaurant, and zipcode

class PromptForCuisineTests(RestaurantDataTestCase):
    def test_prompt_valid_cuisine(self):
        '''
        takes valid string and passes valid (lowercased) string
        '''
        self.assertEqual(prompt_for_cuisine(self.dummy_data, lambda _: "Thai"), "thai")
    
class PromptForRestaurantTests(RestaurantDataTestCase):
    def test_prompt_valid_restaurant(self):
        '''
        takes valid string and passes valid (lowercased) string
        '''
        self.assertEqual(prompt_for_restaurant_name(self.dummy_data, lambda _: "Senor frog", 0), "senor frog")

class PromptForZipTests(RestaurantDataTestCase):
    def test_prompt_valid_zip(self):
        '''
        takes valid zipcode (as string from userinput) and passes valid zipcode (as int)
        '''
        self.assertEqual(prompt_for_zip(self.dummy_data, lambda _: "10011"), "10011")

if __name__ == "__main__":
    unittest.main()
    