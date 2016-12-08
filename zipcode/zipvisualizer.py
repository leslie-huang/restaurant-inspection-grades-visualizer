
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
plt.style.use("ggplot")

class ZipGrades(object):
    def __init__(self, zipcode, data):
        '''
        Constructor
        '''
        self.data = data
        self.zipcode = zipcode

    def get_zip_data(self):
        '''
        Returns a DF subset of the data for the zipcode in question
        '''
        return self.data[self.data["zipcode"] == self.zipcode]
    
    def graph_zip_lettergrade_frequency(self):
        '''
        Generates pie graph of letter grades awarded in cuisine category
        '''
        data = self.get_zip_data()
        grades = ["a", "b", "c", "not yet graded"]
        data = data[data["grade"].isin(grades)]
                
        data.grade.value_counts().plot(kind = "pie", title = "Distribution of Letter Grades in Zipcode: {}".format(self.zipcode), labels = map(lambda x: x.title(), grades))
        plt.xlabel("Grade")
        plt.ylabel("Number of Times Awarded")
        plt.show()
    
    def boxplot_zip_scores(self):
        data = self.get_zip_data()
        plt.boxplot(data["score"], vert = False)
        plt.title("Distribution of Inspection Violations in Zipcode: {}".format(self.zipcode))
        plt.xlabel("Inspection Violation Scores")
        plt.show()
    
    def bargraph_sidewalk(self):
        pass
    
    def make_graphs(self):
        self.graph_zip_lettergrade_frequency()
        self.boxplot_zip_scores()
        