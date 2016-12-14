# Author: Leslie Huang (lh1036)
# Attributes and methods for the zipcode visualizer

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from string import capwords
from .visualizer import Visualizer
plt.style.use("ggplot")

class ZipGrades(Visualizer):
    def __init__(self, zipcode, data):
        '''
        Constructor
        '''
        super(ZipGrades, self).__init__(data)
        self.zipcode = zipcode
        
    ### Methods to subset appropriate data, perform calculations and sort to prepare for graphing

    def filter_data(self, data):
        '''
        Returns a DF subset of the data for the zipcode in question
        '''
        return data[data["zipcode"] == self.zipcode]
        
    ### Methods to generate different visualizations of data
    
    def graph_lettergrade_frequency(self):
        '''
        Generates pie graph of letter grades awarded in cuisine category
        '''
        data = self.filter_data_valid_values("grade", ["A", "B", "C", "Not Yet Graded", "Grade Pending"])
                
        data.grade.value_counts().plot(kind = "pie", title = "Distribution of Letter Grades in Zipcode: {}".format(self.zipcode))
        plt.xlabel("Grade")
        plt.ylabel("Number of Times Awarded")
        
        plt.savefig("{}_restaurant_lettergrades.pdf".format(self.zipcode))
        plt.close()   
            
    def boxplot_zip_scores(self):
        '''
        Boxplot of scores in this zipcode, grouped by sidewalk cafe category
        '''
        grouped = self.group_by_sidewalk()
                
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
                
    def make_graphs(self):
        '''
        Calls all graphing methods for this class
        '''
        self.graph_lettergrade_frequency()
        self.boxplot_zip_scores()
        self.violations_by_category()
        