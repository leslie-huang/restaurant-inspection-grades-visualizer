
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from string import capwords

plt.style.use("ggplot")
pd.options.mode.chained_assignment = None

class CuisineGrades(object):
    def __init__(self, cuisine_name, data):
        '''
        Constructor
        '''
        self.data = data
        self.cuisine_name = cuisine_name

    ### Class methods for subsetting and returning the data
    
    def get_cuisine_data(self):
        '''
        Returns a DF subset of the data for the cuisine in question
        '''
        return self.data[self.data["cuisine_primary"] == self.cuisine_name]
    
    def group_by_sidewalk(self):
        '''
        Returns a GroupBy DF of mean scores by sidewalk cafe type
        '''
        data = self.get_cuisine_data()
        
        # add an index label for restaurants that don't have any sidewalk cafe
        data.loc[:, "swc_type"] = data["swc_type"].replace(np.nan, "no cafe", regex = True)
        
        return data.groupby("swc_type").mean()
    
    def get_lettergrade_data(self):
        '''
        Gets data on lettergrades
        '''
        data = self.get_cuisine_data()
        grades = ["a", "b", "c", "not yet graded", "grade pending"]
        return (data[data["grade"].isin(grades)], grades)
    
    def calculate_mean_by_restaurant(self):
        '''
        Returns a DF of mean inspection violations per restaurant, sorted ascending value
        '''
        data = self.get_cuisine_data()
        data = data.groupby(data.index)[["score"]].mean()
        return data.sort_values(by = "score")
    
    def get_boro_data(self):
        '''
        Gets data on the 5 boroughs and formats labels
        '''
        data = self.get_cuisine_data()
        data["boro"] = data["boro"].apply(capwords)
        boros = ["Manhattan", "Queens", "Bronx", "Brooklyn", "Staten Island"]
        return data[data["boro"].isin(boros)]

    ### Class methods for visualizing the data
    
    def graph_lettergrade_frequency(self):
        '''
        Generates pie graph of letter grades awarded in cuisine category
        '''
        data, grades = self.get_lettergrade_data()
        
        data.grade.value_counts().plot(kind = "pie", title = "Distribution of Letter Grades in Category: {}".format(capwords(self.cuisine_name)), labels = map(capwords, grades), rot = 0)
        plt.xlabel("Grade")
        plt.ylabel("Number of Times Awarded")
        
        plt.savefig("{}_restaurants_lettergrades.pdf".format(capwords(self.cuisine_name)))
        plt.close()   
            
    def boxplot_by_boro(self):
        '''
        Show boxplot of restaurant violations in this category, grouped by borough
        '''
        data = self.get_boro_data()
        
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
        plt.title("Distribution of Inspection Violations by Sidewalk Cafe Type: {}".format(capwords(self.cuisine_name)))
        plt.ylabel("Average Inspection Violation Scores")
        plt.xlabel("Type of Sidewalk Cafe (if any)")
        
        plt.savefig("{}_restaurant_violations_by_cafe_type.pdf".format(capwords(self.cuisine_name)))
        plt.close()    
            
    def violations_per_restaurant(self):
        '''
        Distribution of Mean violations per restaurant
        '''
        data = self.calculate_mean_by_restaurant()
        data.plot(kind = "bar", legend = False)
        plt.title("Distribution of Mean Inspection Violations for {} Restaurants".format(capwords(self.cuisine_name)))
        plt.xticks([])
        plt.ylabel("Mean Inspection Violations Score")
        plt.xlabel("{} Restaurants".format(capwords(self.cuisine_name)))
        
        plt.savefig("{}_restaurant_distribution.pdf".format(capwords(self.cuisine_name)))
        plt.close()    
            
    def make_graphs(self):
        self.graph_lettergrade_frequency()
        self.boxplot_by_boro()
        self.bargraphs_by_sidewalk_type()
        self.violations_per_restaurant()
        