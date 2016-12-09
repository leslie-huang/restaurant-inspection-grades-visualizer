# Author: Leslie Huang (lh1036)
# Description: Helper functions to prompt and handle userinput of year in the "main"

from restaurant.restaurantvisualizer import RestaurantGrades
from cuisine.cuisinevisualizer import CuisineGrades
from zipcode.zipvisualizer import ZipGrades
from exceptions import *

def quitting_input(prompt, input_function = input):
    '''
    Program exits if user types "finish," which raises QuitError
    '''
    userinput = input_function(prompt)
    
    if userinput == "finish":
        raise QuitError()
    
    return userinput
    
def prompt_for_browsechoice(restaurant_data, input_function = input):
    '''
    Prompt user to choose how they want to browse the data, 
    and executes appropriate program
    '''
    choices = {
        "restaurant": (prompt_for_restaurant_name, RestaurantGrades), 
        "cuisine": (prompt_for_cuisine, CuisineGrades), 
        "zipcode": (prompt_for_zip, ZipGrades)
    }
        
    while True:
        try:
            userinput = quitting_input("Enter 'restaurant' to search for a specific restaurant by name, 'zipcode' to visualize grades by zipcode, or 'cuisine' to visualize grades by cuisine category, or 'finish' when you're done.\n", input_function)
            
            prompt, cls = choices[userinput]
            cls(prompt(restaurant_data, input_function), restaurant_data).make_graphs()
        
        except KeyError:
            print("Try again.\n")

def prompt_for_cuisine(restaurant_data, input_function = input):
    '''
    Prompt user for year. Repeats prompt until "finish" is entered.
    @param restaurant_data: restaurant_data DF
    @param input_function: default is the Python input method; this is to allow for unittesting
    '''
    
    while True:
        try:
            userinput = quitting_input("Please enter a cuisine category or 'finish' if you are done.\n", input_function)
            return validate_cuisine(userinput, restaurant_data)
            
        except InvalidCuisineError as e:
            print(e)

def validate_cuisine(input_cuisine, restaurant_data):
    '''
    Validate that user input is a valid cuisine that appears in restaurant_data.primary_cuisine
    Raises InvalidCuisineError if (1) input is not in data or (2) input is invalid type (e.g. an int)
    '''
    
    try:
        cuisine = input_cuisine.lower()
        
        if cuisine not in restaurant_data.cuisine_primary.unique():
            raise InvalidCuisineError()
        
        else:
            return cuisine
            
    except AttributeError:
        raise InvalidCuisineError()


def prompt_for_zip(restaurant_data, input_function = input):
    '''
    Prompt user for zipcode. Repeats prompt until "finish" is entered.
    @param restaurant_data: restaurant_data DF
    @param input_function: default is the Python input method; this is to allow for unittesting
    '''
    
    while True:
        try:
            userinput = quitting_input("Please enter a zipcode or 'finish' if you are done.", input_function)
            return validate_zip(userinput, restaurant_data)
            
        except InvalidZipError as e:
            print(e)

def validate_zip(input_zip, restaurant_data):
    '''
    Validate that user input is a valid zipcode that appears in the data
    Raises InvalidCuisineError if (1) input is not in data or 
    (2) input is invalid type (e.g. a string)
    '''
    
    try:
        zipcode = int(input_zip)
        
        if zipcode not in restaurant_data.zipcode.astype(int).unique():
            raise InvalidZipError()
        
        else:
            return zipcode
            
    except ValueError:
        raise InvalidZipError()

def prompt_for_restaurant_name(restaurant_data, input_function = input):
    '''
    Prompt user for restaurant name. Repeats prompt until "finish" is entered.
    @param restaurant_data: restaurant_data DF
    @param input_function: default is the Python input method; this is to allow for unittesting
    '''
    
    while True:
        try:
            userinput = quitting_input("Please enter a restaurant name or 'finish' if you are done.", input_function)
            return validate_restaurant_name(userinput, restaurant_data)
            
        except InvalidRestaurantNameError as e:
            print(e)
    

def validate_restaurant_name(input_name, restaurant_data):
    '''
    Validate that user input is a valid restaurant that appears in restaurant_data
    Raises InvalidRestaurantNameError if (1) input is not in data or 
    (2) input is invalid type (e.g. an int)
    '''
    
    try:
        restaurant_name = input_name.lower()
        
        if restaurant_name not in restaurant_data.index.unique():
            raise InvalidRestaurantNameError()
        
        else:
            return restaurant_name
            
    except AttributeError:
        raise InvalidRestaurantNameError()