# Author: Leslie Huang (lh1036)
# Attributes and methods for the cuisine visualizer

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from .visualizer import Visualizer
from string import capwords

plt.style.use("ggplot")
pd.options.mode.chained_assignment = None

class CuisineGrades(Visualizer):
    def __init__(self, cuisine_name, data):
        '''
        Constructor
        '''
        super(CuisineGrades, self).__init__(data)
        self.cuisine_name = cuisine_name

    ### Class methods for subsetting and returning the data
    
    def filter_data(self, data):
        '''
        Returns a DF subset of the data for the cuisine in question
        '''
        return data[data["cuisine_primary"] == self.cuisine_name]

    ### Class methods for visualizing the data
    
    def graph_lettergrade_frequency(self):
        '''
        Generates pie graph of letter grades awarded in cuisine category
        '''
        data = self.filter_data_valid_values("grade", ["A", "B", "C", "Not Yet Graded", "Grade Pending"])
        
        data.grade.value_counts().plot(kind = "pie", title = "Distribution of Letter Grades for {} Restaurants".format(capwords(self.cuisine_name)), rot = 0)
        plt.xlabel("Grade")
        plt.ylabel("Number of Times Awarded")
        
        plt.savefig("{}_restaurants_lettergrades.pdf".format(capwords(self.cuisine_name)))
        plt.close()   
            
    def boxplot_by_boro(self):
        '''
        Show boxplot of restaurant violations in this category, grouped by borough
        '''
        data = self.filter_data_valid_values("boro", ["Manhattan", "Queens", "Bronx", "Brooklyn", "Staten Island"])
        
        data.boxplot(by = "boro", column = "score", return_type = "dict", rot = 90)
        plt.xlabel("Boroughs")
        plt.ylabel("Inspection Violations")
        plt.subplots_adjust(bottom = 0.3)
    
        # add title and get rid of automatically added title
        plt.title("Spread of Violations by Borough for {} Restaurants".format(capwords(self.cuisine_name)))
        plt.suptitle("")
        plt.savefig("{}_restaurant_violations_by_borough.pdf".format(capwords(self.cuisine_name)))
        plt.close()    
        
    def bargraphs_by_sidewalk_type(self):
        '''
        Show bargraph of average violations by sidewalk cafe type
        '''
        grouped = self.group_by_sidewalk()
                
        grouped.score.plot(kind = "bar", rot = 90)
        plt.subplots_adjust(bottom = 0.5)
        plt.title("Inspection Violations by Cafe Type for {} Restaurants".format(capwords(self.cuisine_name)))
        plt.ylabel("Average Inspection Violation Scores")
        plt.xlabel("Type of Sidewalk Cafe (if any)")
        plt.savefig("{}_restaurant_violations_by_cafe_type.pdf".format(capwords(self.cuisine_name)))
        plt.close()    
            
    def violations_per_restaurant(self):
        '''
        Distribution of mean violations per restaurant
        '''
        data = self.calculate_mean_by_restaurant()
        data.plot(kind = "bar", legend = False)
        plt.title("Distribution of Mean Inspection Violations for {} Restaurants".format(capwords(self.cuisine_name)))
        plt.xticks([])
        plt.ylabel("Mean Inspection Violations Score")
        plt.xlabel("{} Restaurants".format(capwords(self.cuisine_name)))
        
        plt.savefig("{}_restaurant_distribution.pdf".format(capwords(self.cuisine_name)))
        plt.close() 
    
    def timeseries_best_and_worst(self):
        '''
        Timeseries of inspection scores for the best and worst restaurants in this zip
        Restricted to restaurants with at least 15 inspections (to exclude outliers)
        Remember, lower is better! Higher score = more violations = dirty restaurant
        '''
        best_data, worst_data, = self.get_best_and_worst_data(15)
        best_name, worst_name = self.get_best_and_worst_names(15)
        x_best, y_best = best_data["inspectiondate"], best_data["score"]
        x_worst, y_worst = worst_data["inspectiondate"], worst_data["score"]

        plt.plot_date(x = x_best, y = y_best, fmt = "r-", label = "{}".format(capwords(best_name)))
        plt.plot_date(x = x_worst, y = y_worst, fmt = "b-", label = "{}".format(capwords(worst_name)))
        plt.xticks(rotation = "vertical")
        
        plt.legend(loc = "upper right")
        plt.ylabel("Inspection Violations Score")
        plt.title("Time Series of Inspection Violations for the Best ({}) \n and Worst ({}) {} Restaurants".format(capwords(best_name), capwords(worst_name), capwords(self.cuisine_name)))
        
        plt.annotate("Best and worst restaurants have the lowest and highest mean inspection violations, respectively. \nTo exclude outliers, only restaurants that have received at least 10 inspections are considered.", (0,0), (0, -100), xycoords = "axes fraction", textcoords = "offset points", va = "top")
        plt.subplots_adjust(bottom = 0.5)
        
        plt.savefig("{}_best_worst_restaurants_timeseries.pdf".format(capwords(self.cuisine_name)))
        plt.close()   
            
    def make_graphs(self):
        '''
        Calls all graphing methods for this class
        '''
        self.graph_lettergrade_frequency()
        self.boxplot_by_boro()
        self.bargraphs_by_sidewalk_type()
        self.violations_per_restaurant()
        self.timeseries_best_and_worst()
        