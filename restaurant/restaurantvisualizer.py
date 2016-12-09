
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
        Returns a DF subset for the specified restaurant, sorted by date
        '''
        return self.data.ix[self.restaurant_name].sort_values(by = "inspectiondate")
    
    def get_lettergrades(self):
        '''
        Returns a DF of lettergrades formatted for graphing
        '''
        data = self.get_restaurant_data()
        grades = ["a", "b", "c", "not yet graded"]
        data = data[data["grade"].isin(grades)]
        data["grade"] = data["grade"].apply(lambda x: x.title())
        return data

    def graph_restaurant_timeseries(self):
        '''
        Plots a line graph of inspection violation scores over time
        '''
        data = self.get_restaurant_data()
        y = data["score"]
        x = data["inspectiondate"]
    
        plt.plot_date(x = x, y = y, fmt = "r-")
        plt.ylabel("Inspection Violations")
        plt.title("Inspection Violations at {} Over Time".format(self.restaurant_name.title()))
        plt.show()
    
    def graph_restaurant_lettergrade_frequency(self):
        '''
        Plots a bar graph of frequency of letter grades
        '''
        data = self.get_lettergrades()
        print(data.head())
        
        data["grade"].value_counts().plot(kind = "bar", title = "Letter Grades Awarded to {}".format(self.restaurant_name.title()))
        plt.xlabel("Grade")
        plt.ylabel("Number of Times Awarded")
        plt.show()
        
    def make_graphs(self):
        self.graph_restaurant_timeseries()
        self.graph_restaurant_lettergrade_frequency()
        