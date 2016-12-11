
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from string import capwords
from .visualizer import Visualizer
plt.style.use("ggplot")

class RestaurantGrades(Visualizer):
    def __init__(self, restaurant_name, data):
        '''
        Constructor
        '''
        super(RestaurantGrades, self).__init__(data)
        self.restaurant_name = restaurant_name
        
    ### Class methods for subsetting and returning the data

    def filter_data(self):
        '''
        Returns a DF subset for the specified restaurant, sorted by date
        '''
        return self.data.ix[self.restaurant_name].sort_values(by = "inspectiondate")
    
    ### Class methods for visualizing the data

    def graph_restaurant_timeseries(self):
        '''
        Plots a line graph of inspection violation scores over time
        '''
        data = self.filter_data()        
        
        plt.plot_date(x = data["inspectiondate"], y = data["score"], fmt = "r-")
        plt.xticks(rotation = "vertical")
        plt.ylabel("Inspection Violations")
        plt.title("Inspection Violations at {} Over Time".format(capwords(self.restaurant_name)))
        
        plt.annotate("Note: Graph includes all restaurants named {}.".format(capwords(self.restaurant_name)), (0,0), (0, -100), xycoords = "axes fraction", textcoords = "offset points", va = "top")
        plt.subplots_adjust(bottom = 0.5)
        
        plt.savefig("{}_timeseries.pdf".format(capwords(self.restaurant_name)))
        plt.close()   
            
    def graph_restaurant_lettergrade_frequency(self):
        '''
        Plots a bar graph of frequency of letter grades received
        '''
        data = self.get_lettergrade_data()
        
        data["grade"].value_counts().plot(kind = "bar", rot = 0, title = "Letter Grades Awarded to {}".format(capwords(self.restaurant_name)))
        plt.xlabel("Grade")
        plt.ylabel("Number of Times Awarded")
        
        plt.annotate("Note: Graph includes all restaurants named {}.".format(capwords(self.restaurant_name)), (0,0), (0, -50), xycoords = "axes fraction", textcoords = "offset points", va = "top")
        plt.subplots_adjust(bottom = 0.3)
        
        plt.savefig("{}_lettergrades.pdf".format(capwords(self.restaurant_name)))
        plt.close()   
                
    def make_graphs(self):
        '''
        Calls all graphing methods for this class
        '''
        self.graph_restaurant_timeseries()
        self.graph_restaurant_lettergrade_frequency()
        