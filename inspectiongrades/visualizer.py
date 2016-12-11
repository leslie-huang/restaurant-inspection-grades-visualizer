# Superclass of the cuisine, restaurant, and zipcode visualizers

from string import capwords
import pandas as pd

class Visualizer(object):
    def __init__(self, data):
        self.data = data
    
    def filter_data(self, data):
        raise NotImplementedError()
        
    def group_by_sidewalk(self):
        '''
        Returns a GroupBy DF of mean scores by sidewalk cafe type
        '''
        data = self.filter_data()
        
        return data.groupby("swc_type").mean()
    
    def get_lettergrade_data(self):
        '''
        Gets lettergrade data and formats labels for graphing
        '''
        data = self.filter_data()
        grades = ["a", "b", "c", "not yet graded", "grade pending"]
        data = data[data["grade"].isin(grades)]
        data["grade"] = data["grade"].apply(capwords)
        return data    
            
    def get_boro_data(self):
        '''
        Restricts data to 5 boroughs and formats labels
        '''
        data = self.filter_data()
        data["boro"] = data["boro"].apply(capwords)
        boros = ["Manhattan", "Queens", "Bronx", "Brooklyn", "Staten Island"]
        return data[data["boro"].isin(boros)]
        
    def calculate_mean_by_restaurant(self):
        '''
        Returns a DF of mean inspection violations per restaurant, sorted ascending value
        Used in the cuisinevisualizer
        '''
        data = self.filter_data()
        data = data.groupby(data.index)[["score"]].mean()
        return data.sort_values(by = "score")
    
    def group_scores_by_category(self):
        '''
        Returns a GroupBy DF of mean violation score per cuisine category
        Used in the zipvisualizer
        '''
        data = self.filter_data()
        grouped = data.groupby("cuisine_primary").mean()
        grouped.index = pd.Index(capwords(cuisine) for cuisine in grouped.index)
        return grouped.sort_values(by = "score")
    
        
    def get_best_and_worst_names(self):
        '''
        Returns a list of 2 restaurants with lowest and highest mean inspection violations score
        Restricted to restaurants with at least 10 inspection scores (to exclude outliers)
        Used in zipvisualizer and cuisinevisualizer
        '''
        data = self.filter_data()
        # get names of highest and lowest restaurants
        grouped = data.groupby(data.index).agg(["mean", "count"])["score"]
        grouped = grouped.sort_values(by = "mean")
        grouped = grouped[grouped["count"] >= 10]
        names = [grouped.index[0], grouped.index[-1]]
        return names
    
        
    def get_best_and_worst_data(self):
        '''
        Returns a tuple containing (DF of best restaurant, DF of worst restaurant)
        Used in zipvisualizer
        '''
        data = self.filter_data()
        data = data[data.index.isin(self.get_best_and_worst_names())]
        data = data.sort_values(by = "inspectiondate")
        best_name, worst_name = self.get_best_and_worst_names()
        return (data[data.index.isin([best_name])], data[data.index.isin([worst_name])])
    
    