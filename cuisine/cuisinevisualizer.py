
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
plt.style.use("ggplot")
pd.options.mode.chained_assignment = None

class CuisineGrades(object):
    def __init__(self, cuisine_name, data):
        '''
        Constructor
        '''
        self.data = data
        self.cuisine_name = cuisine_name

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
        data.loc[:, "swc_type"] = data["swc_type"].replace("", "no cafe", regex = True)
        
        return data.groupby("swc_type").mean()
    
    def calculate_mean_by_restaurant(self):
        '''
        Returns a DF of mean inspection violations per restaurant, sorted ascending value
        '''
        data = self.get_cuisine_data()
        data = data.groupby(data.index)[["score"]].mean()
        return data.sort_values(by = "score")
    
    def graph_lettergrade_frequency(self):
        '''
        Generates pie graph of letter grades awarded in cuisine category
        '''
        data = self.get_cuisine_data()
        grades = ["a", "b", "c", "not yet graded"]
        data = data[data["grade"].isin(grades)]
        
        data.grade.value_counts().plot(kind = "pie", title = "Distribution of Letter Grades in Category: {}".format(self.cuisine_name.title()), labels = map(lambda x: x.title(), grades))
        plt.xlabel("Grade")
        plt.ylabel("Number of Times Awarded")
        plt.show()
    
    def boxplot_by_boro(self):
        '''
        Show boxplot of restaurant violations in this category, grouped by borough
        '''
        self.data.boxplot(by = "boro", column = "score", return_type = "dict", rot = 90)
        plt.xlabel("Boroughs")
        plt.ylabel("Inspection Violations")
        #plt.subplots_adjust(bottom = 0.3)
    
        # add title and get rid of automatically added title
        plt.title("Spread of Violations by Borough for {} Restaurants".format(self.cuisine_name))
        plt.suptitle("")
        
        plt.show()
    
    def bargraphs_by_sidewalk_type(self):
        '''
        Show bargraph of average violations by sidewalk cafe type
        '''
        grouped = self.group_by_sidewalk()
                
        grouped.score.plot(kind = "bar", rot = 90)
        plt.subplots_adjust(bottom = 0.5)
        plt.title("Distribution of Inspection Violations by Sidewalk Cafe Type: {}".format(self.cuisine_name.title()))
        plt.ylabel("Average Inspection Violation Scores")
        plt.xlabel("Type of Sidewalk Cafe (if any)")
        plt.show()
    
    def violations_per_restaurant(self):
        '''
        Distribution of average violations per restaurant
        '''
        data = self.calculate_mean_by_restaurant()
        data.plot(kind = "bar")
        plt.xticks([])
        
        plt.show()
    
    def make_graphs(self):
        self.graph_lettergrade_frequency()
        self.boxplot_by_boro()
        self.bargraphs_by_sidewalk_type()
        self.violations_per_restaurant()
        