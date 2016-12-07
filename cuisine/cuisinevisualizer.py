
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
plt.style.use("ggplot")

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
    
    def graph_cuisine_lettergrade_frequency(self):
        '''
        Generates pie graph of letter grades awarded in cuisine category
        '''
        data = self.get_cuisine_data()
        data = data[data["grade"].isin(["a", "b", "c"])]
        
        data.grade.value_counts().plot(kind = "pie", title = "Distribution of Letter Grades in Category: {}".format(self.cuisine_name))
        plt.xlabel("Grade")
        plt.ylabel("Number of Times Awarded")
        plt.show()
    
    def boxplot_cuisine_scores(self):
        data = self.get_cuisine_data()
        plt.boxplot(data["score"], vert = False)
        plt.title("Distribution of Inspection Violations in Category: {}".format(self.cuisine_name))
        plt.xlabel("Inspection Violation Scores")
        plt.show()
    
    def bargraph_sidewalk(self):
        pass
    
    def make_graphs(self):
        self.graph_cuisine_lettergrade_frequency()
        self.boxplot_cuisine_scores()
        