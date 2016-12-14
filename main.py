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
restaurant_data = clean_data()
restaurant_data = restaurant_data.set_index(["restaurant"])

if __name__ == "__main__":

    try:
        while True:
            prompt_for_browsechoice(restaurant_data)

    except (QuitError, KeyboardInterrupt):
        pass