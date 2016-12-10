
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from string import capwords
plt.style.use("ggplot")

class ZipGrades(object):
    def __init__(self, zipcode, data):
        '''
        Constructor
        '''
        self.data = data
        self.zipcode = zipcode
        
    ### Methods to subset appropriate data, perform calculations and sort to prepare for graphing

    def get_zip_data(self):
        '''
        Returns a DF subset of the data for the zipcode in question
        '''
        return self.data[self.data["zipcode"] == self.zipcode]
    
    def group_scores_by_sidewalk(self):
        '''
        Returns a GroupBy DF of mean scores by sidewalk cafe type
        '''
        data = self.get_zip_data()
        
        # add an index label for restaurants that don't have any sidewalk cafe
        data.loc[:, "swc_type"] = data["swc_type"].replace(np.nan, "no cafe", regex = True)
        
        return data.groupby("swc_type").mean()
    
    def get_lettergrade_data(self):
        '''
        Gets data on lettergrades
        '''
        data = self.get_zip_data()
        grades = ["a", "b", "c", "not yet graded", "grade pending"]
        return data[data["grade"].isin(grades)]
        
    def group_scores_by_category(self):
        '''
        Returns a GroupBy DF of mean violation score per cuisine category
        '''
        data = self.get_zip_data()
        grouped = data.groupby("cuisine_primary").mean()
        grouped.index = pd.Index(capwords(cuisine) for cuisine in grouped.index)
        return grouped.sort_values(by = "score")
    
    def get_best_and_worst_names(self):
        '''
        Returns a list of 2 restaurants with lowest and highest mean inspection violations score
        Restricted to restaurants with at least 10 inspection scores (to exclude outliers)
        '''
        data = self.get_zip_data()
        # get names of highest and lowest restaurants
        grouped = data.groupby(data.index).agg(["mean", "count"])["score"]
        grouped = grouped.sort_values(by = "mean")
        grouped = grouped[grouped["count"] >= 10]
        names = [grouped.index[0], grouped.index[-1]]
        return names
    
    def get_best_and_worst_data(self):
        '''
        Returns a tuple containing (DF of best restaurant, DF of worst restaurant)
        '''
        data = self.get_zip_data()
        data = data[data.index.isin(self.get_best_and_worst_names())]
        data = data.sort_values(by = "inspectiondate")
        best_name, worst_name = self.get_best_and_worst_names()
        return (data[data.index.isin([best_name])], data[data.index.isin([worst_name])])
    
    ### Methods to generate different visualizations of data
    
    def graph_lettergrade_frequency(self):
        '''
        Generates pie graph of letter grades awarded in cuisine category
        '''
        data = self.get_zip_data()
        grades = ["a", "b", "c", "not yet graded"]
        data = data[data["grade"].isin(grades)]
                
        data.grade.value_counts().plot(kind = "pie", title = "Distribution of Letter Grades in Zipcode: {}".format(self.zipcode), labels = map(capwords, grades))
        plt.xlabel("Grade")
        plt.ylabel("Number of Times Awarded")
        
        plt.savefig("{}_restaurant_lettergrades.pdf".format(self.zipcode))
        plt.close()   
            
    def boxplot_zip_scores(self):
        '''
        Boxplot of scores in this zipcode, grouped by sidewalk cafe category
        '''
        grouped = self.group_scores_by_sidewalk()
                
        grouped.score.plot(kind = "bar", rot = 90)
        plt.subplots_adjust(bottom = 0.5)
        plt.title("Distribution of Inspection Violations by Sidewalk Cafe Type in {}".format(self.zipcode))
        plt.ylabel("Average Inspection Violation Scores")
        plt.xlabel("Type of Sidewalk Cafe (if any)")
        
        plt.savefig("{}_restaurant_scores_by_cafe_type.pdf".format(self.zipcode))
        plt.close()           
        
    def violations_by_category(self):
        '''
        Generates a bar graph of inspection violations by category in this zipcode
        '''
        grouped = self.group_scores_by_category()
        grouped.score.plot(kind = "barh")
        plt.xlabel("Inspection Violation Scores")
        plt.ylabel("Cuisine")
        plt.title("Mean Inspection Violations for Cuisine Categories in {}".format(self.zipcode))
        
        plt.savefig("{}_restaurant_violations_by_category.pdf".format(self.zipcode))
        plt.close()   
                
    def timeseries_best_and_worst(self):
        '''
        Timeseries of inspection scores for the best and worst restaurants in this zip
        Remember, lower is better! Higher score = more violations = dirty restaurant
        '''
        best_data, worst_data, = self.get_best_and_worst_data()
        best_name, worst_name = self.get_best_and_worst_names()
        x_best, y_best = best_data["inspectiondate"], best_data["score"]
        x_worst, y_worst = worst_data["inspectiondate"], worst_data["score"]

        plt.plot_date(x = x_best, y = y_best, fmt = "r-", label = "{}".format(capwords(best_name)))
        plt.plot_date(x = x_worst, y = y_worst, fmt = "b-", label = "{}".format(capwords(worst_name)))
        plt.xticks(rotation = "vertical")
        
        plt.legend(loc = "upper right")
        plt.ylabel("Inspection Violations Score")
        plt.title("Time Series of Inspection Violations for the Best ({}) \n and Worst ({}) Restaurants Located in {}".format(capwords(best_name), capwords(worst_name), self.zipcode))
        
        plt.annotate("Best and worst restaurants have the lowest and highest mean inspection violations, respectively. \nTo exclude outliers, only restaurants that have received at least 10 inspections are considered.", (0,0), (0, -100), xycoords = "axes fraction", textcoords = "offset points", va = "top")
        plt.subplots_adjust(bottom = 0.5)
        
        plt.savefig("{}_zip_best_worst_restaurants_timeseries.pdf".format(self.zipcode))
        plt.close()   
            
    def make_graphs(self):
        self.graph_lettergrade_frequency()
        self.boxplot_zip_scores()
        self.violations_by_category()
        self.timeseries_best_and_worst()
        