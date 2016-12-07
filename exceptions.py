# Author: Leslie Huang (lh1036)
# Description: Custom errors for handling user input

class InvalidCuisineError(Exception):
    '''
    Error if user inputs a cuisine not contained in dataset
    '''
        
    def __str__(self):
        return "Cuisine not in list. Try something like 'pizza' or 'Japanese'."

class InvalidZipError(Exception):
    '''
    Error if user inputs a zipcode not in NYC
    '''
    def __str__(self):
        return "Zipcode not in NYC. Try something like 10013."

class InvalidRestaurantNameError(Exception):
    '''
    Error if user inputs a restaurant not in the dataset
    '''
    def __str__(self):
        return "We can't find a restaurant by that name. Try something like 'Tacombi'."

class QuitError(Exception):
    '''
    Error if user ends program with input "finish" or if Keyboard Interrupt
    '''

    def __str__(self):
        return "Goodbye."