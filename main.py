# Author: Leslie Huang (lh1036)
# Description: Main for the Restaurant Grades Explorer.
# This program loads in the cleaned dataset and uses interactive 
# prompts to allow the user to search by restaurant name, cuisine 
# category, or zip code. The program will generate data visualizations 
# based on the user's request.  

import pandas as pd
import numpy as np
from userinput import *
from datacleaning import clean_data

### Set up the DF for analysis
#restaurant_data = pd.read_csv("cleaned_data.csv", keep_default_na = False, na_values = [])
restaurant_data = clean_data()
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