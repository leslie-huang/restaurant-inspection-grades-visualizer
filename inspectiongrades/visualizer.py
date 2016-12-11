# Author: Leslie Huang (lh1036)
# Attributes and methods for the Visualizer class, a superclass of the cuisine, restaurant, and zipcode visualizers

from string import capwords
import pandas as pd

class Visualizer(object):
    def __init__(self, data):
        self.data = data
    
    def filter_data(self, data):
        '''
        Each child class will override this method with a custom filter_data
        '''
        return data
        
    ### Classmethods that subset, sort, and perform calculations on data to prepare for graphing
    
    def filter_data_valid_values(self, column_name, valid_values):
        '''
        @param data: Automatically set to the filtered base dataset for each class
        @param column_name: The column we are using to filter observations
        @param valid_values: A list of valid values for observations in column_name (others will be dropped)
        Also formats capitalization of the values (because dataframe is all lowecase)
        '''
        data = self.filter_data(self.data)
        data[column_name] = data[column_name].apply(capwords)
        return data[data[column_name].isin(valid_values)]
        
    def calculate_mean_by_restaurant(self):
        '''
        Returns a DF of mean inspection violations per restaurant, sorted ascending value
        Used in the cuisinevisualizer
        '''
        data = self.filter_data(self.data)
        data = data.groupby(data.index)[["score"]].mean()
        return data.sort_values(by = "score")
    
    def group_scores_by_category(self):
        '''
        Returns a GroupBy DF of mean violation score per cuisine category and formats category names
        Used in the zipvisualizer
        '''
        
        data = self.filter_data(self.data)
        grouped = data.groupby("cuisine_primary").mean()
        grouped.index = pd.Index(capwords(cuisine) for cuisine in grouped.index)
        return grouped.sort_values(by = "score")
    
    def group_by_sidewalk(self):
        '''
        Returns a GroupBy DF of mean scores by sidewalk cafe type
        '''
        data = self.filter_data(self.data)
        
        return data.groupby("swc_type").mean()
    
    def get_best_and_worst_names(self, minimum_obs):
        '''
        Returns a list of 2 restaurants with lowest and highest mean inspection violations score
        @param minimum_obs: restrict to restaurants with a certain number of inspections
        Used in zipvisualizer and cuisinevisualizer
        '''
        data = self.filter_data(self.data)
        
        # get names of highest and lowest restaurants and filter out restaurants without enough obs
        grouped = data.groupby(data.index).agg(["mean", "count"])["score"]
        grouped = grouped.sort_values(by = "mean")
        grouped = grouped[grouped["count"] >= minimum_obs]
        names = [grouped.index[0], grouped.index[-1]]
        
        return names
        
    def get_best_and_worst_data(self, minimum_obs):
        '''
        Returns a tuple containing (DF of best restaurant, DF of worst restaurant)
        Used in zipvisualizer
        '''
        
        data = self.filter_data(self.data)
        
        # get the best and worst restaurants' names and DF
        best_name, worst_name = self.get_best_and_worst_names(minimum_obs)
        data = data[data.index.isin(self.get_best_and_worst_names(minimum_obs))]
        data = data.sort_values(by = "inspectiondate") # sorting needed for timeseries line graph
        
        return (data[data.index.isin([best_name])], data[data.index.isin([worst_name])])
    
    