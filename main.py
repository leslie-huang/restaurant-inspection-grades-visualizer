# Author: Leslie Huang (lh1036)
# Description: This program runs the 

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from cuisine.cuisinevisualizer import CuisineGrades
from restaurant.restaurantvisualizer import RestaurantGrades
from zipcode.zipvisualizer import ZipGrades
from userinput import *

plt.style.use("ggplot")

### Set up the DFs for analysis
restaurant_data = pd.read_csv("cleaned_data.csv", keep_default_na = False, na_values = []).drop(["Unnamed: 0"], axis = 1)
restaurant_data = restaurant_data.set_index(["restaurant"])

# convert date to datetime object for timeseries analysis
for col_name in ["inspectiondate", "gradedate", "issuance_dd"]:
    restaurant_data[col_name] = pd.to_datetime(restaurant_data[col_name], format = "%m/%d/%Y", errors = "coerce")

if __name__ == "__main__":
    
    try:
        while True:
            prompt_for_browsechoice(restaurant_data)

    
    except (QuitError, KeyboardInterrupt):
        pass