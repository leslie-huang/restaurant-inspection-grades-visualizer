
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
plt.style.use("ggplot")

class RestaurantGrades(object):
    def __init__(self, restaurant_name, data):
        '''
        Constructor
        '''
        self.data = data
        self.restaurant_name = restaurant_name

    def get_restaurant_data(self):
        '''
        Returns a DF subset of the data for the restaurant in question
        '''
        return self.data.ix[self.restaurant_name]

    def graph_restaurant_timeseries(self):
        data = self.get_restaurant_data()
        y = data["score"]
        x = data["inspectiondate"]
    
        plt.plot_date(x = x, y = y)
        plt.ylabel("Inspection Violations")
        plt.title("Inspection Violations at {} Over Time".format(self.restaurant_name))
        plt.show()
    
    def graph_restaurant_lettergrade_frequency(self):
        data = self.get_restaurant_data()
        data = data[data["grade"].isin(["A", "B", "C", "Not Yet Graded"])]
        data.grade.value_counts().plot(kind = "hist", title = "Letter Grades Awarded to {}".format(self.restaurant_name))
        plt.xlabel("Grade")
        plt.ylabel("Number of Times Awarded")
        plt.show()
        
    def make_graphs(self):
        self.graph_restaurant_timeseries()
        self.graph_restaurant_lettergrade_frequency()
        