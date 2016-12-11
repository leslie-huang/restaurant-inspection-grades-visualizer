#!/usr/bin/env python3
# Author: Leslie Huang (lh1036)
# Description: This program imports raw data files 
# (#1: Restaurant Grades Data, #2: Sidewalk Cafe Data), 
# implements data cleaning, and saves the cleaned and merged file.
#
# When this file is run, it will output a CSV of the dataset.
# When this program is called from main.py, it generates a dataframe 
# used within the main.
#
# Note: I have written all non-trivial data cleaning as functions to allow for 
# unit testing. However, data cleaning is specific to the messiness of the data; however, 
# I did not write functions or unittests for the execution of simple Pandas methods.

import pandas as pd
import numpy as np
import re
import zipfile

### Helper functions for data cleaning

def clean_colnames(df):
    # change column names to lowercase and strip whitespace for consistency
    df.columns = pd.Index(col_name.lower().replace(" ", "") for col_name in df.columns)
    return df

def convert_lowercase(df):
    # lowercase all strings in a DF (aids case-insensitive matching to user inputs in main)
    df = pd.concat([df[col].str.lower() for col in df.columns], axis = 1)
    return df
    
def strip_whitespace(df, columns):
    # remove excessive whitespace (typos such as "44th    street") from specified columns
    for col in columns:
        df[col] = pd.Series(" ".join(entry.split()) for entry in df[col])
    return df    

def concat_cols(df, columns_to_add, new_column):
    # create a new string column from an list of existing columns
    df[new_column] = df[columns_to_add].apply(lambda x: " ".join(x), axis = 1)
    return df

def make_primary_cuisine(df, cuisines, cuisine_primary):
    # make a new var (cuisine_primary) that is the first cuisine listed in cuisines
    df[cuisine_primary] = df[cuisines].apply(lambda x: re.split(r"[,/()]", x)[0].strip())   
    return df

def drop_multiple_column_nulls(df, cols_to_drop):
    # drop all observations containing a null in any column in the list cols_to_drop
    for col in cols_to_drop:
        df = df[pd.notnull(df[col])]
    return df

### This is the main datacleaning

def clean_data():
    
    ### read in (1) ZIP archive of Restaurant Inspection Dataset downloaded from  https://data.cityofnewyork.us/Health/DOHMH-New-York-City-Restaurant-Inspection-Results/xx67-kt59
    # PLEASE NOTE: The online version located at that URL is regularly updated. 
    # I use the 11/27/16 version (ZIP = 25 MB, uncompressed CSV = 160 MB)
    with zipfile.ZipFile("DOHMH_New_York_City_Restaurant_Inspection_Results.csv.zip", "r") as myzipfile:
        myzipfile.extractall()
    
    restaurant_grades = pd.read_csv("DOHMH_New_York_City_Restaurant_Inspection_Results.csv", dtype = str, keep_default_na = False, na_values = [])
    
    ### Because of the dataset's size, processing time is nontrivial. Thus, I proceed in the following steps:
    # (1) Fixing names and formatting, so that references are consistent
    # (2) drop rows and columns that won't be used, to reduce the size of the DF that undergoes cleaning
    # (3) cleaning
    
    ### (1) Fixing names and formatting
    restaurant_grades = clean_colnames(restaurant_grades)
    restaurant_grades = restaurant_grades.rename(columns = {"dba": "restaurant"})
    restaurant_grades = strip_whitespace(restaurant_grades, ["street", "restaurant"])
    
    ### (2) Dropping
    
    ## drop unneeded columns
    restaurant_grades = restaurant_grades.drop(["recorddate", "camis", "action", "phone", "violationcode"], axis = 1)
    
    ## Drop rows:
    restaurant_grades = restaurant_grades.drop_duplicates()

    # Missing essential information: (a) name, category, address, or both score and grade
    restaurant_grades = drop_multiple_column_nulls(restaurant_grades, ["restaurant", "street", "cuisinedescription"])
    restaurant_grades = restaurant_grades[pd.notnull(restaurant_grades["score"]) | pd.notnull(restaurant_grades["grade"])]
    
    # drop observations with negative scores (data entry error)
    restaurant_grades = restaurant_grades.loc[pd.to_numeric(restaurant_grades["score"], errors = "ignore") >= 0]
    
    ### (3) Cleanup
    
    # clean up whitespace and lowercase entire DF
    restaurant_grades = convert_lowercase(restaurant_grades)
    
    # format scores and grades
    restaurant_grades["score"] = pd.to_numeric(restaurant_grades["score"])
    restaurant_grades["grade"].replace(to_replace = ["p", "z"], value = "grade pending", inplace = True)
    
    # create unique ID var from address
    restaurant_grades = concat_cols(restaurant_grades, ["building", "street", "zipcode"], "address_id")
    
    # set first-listed cuisine as the primary cuisine and fix a unicode rendering error
    restaurant_grades = make_primary_cuisine(restaurant_grades, "cuisinedescription", "cuisine_primary")
    restaurant_grades["cuisine_primary"].replace(to_replace = ["cafÃ£Â©", "cafã©"], value = "cafe", inplace = True)  
      
      
    ### Read in (2) Sidewalk Cafe Dataset, downloaded from
    # https://data.cityofnewyork.us/Business/Sidewalk-Caf-Licenses-and-Applications/qcdj-rwhu
    # NOTE: This dataset is constantly updated. I use the 12/2/2016 version.
    
    sidewalk_licenses = pd.read_csv("Sidewalk_Caf__Licenses_and_Applications.csv", dtype = str, keep_default_na = False, na_values = [])

    # lowercase and strip whitespace
    sidewalk_licenses = clean_colnames(sidewalk_licenses)
    sidewalk_licenses = convert_lowercase(sidewalk_licenses)
    sidewalk_licenses = strip_whitespace(sidewalk_licenses, ["street", "business_name", "business_name2"])

    # create unique ID var from address
    sidewalk_licenses = concat_cols(sidewalk_licenses, ["building", "street", "zip"], "address_id")

    # Keep only needed columns
    # Note: I drop "building", "street", "zip" AFTER using them to construct address_id
    sidewalk_licenses = sidewalk_licenses[["lic_status", "swc_type", "swc_sq_ft", "issuance", "business_name", "business_name2", "issuance_dd", "address_id"]]


### Merge and output the merged file

    # merge on unique address_id var
    merged = pd.merge(restaurant_grades, sidewalk_licenses, left_on = "address_id", right_on = "address_id", how = "left")
    
    # add a label for restaurants that don't have sidewalk cafes
    merged["swc_type"] = merged["swc_type"].replace(np.nan, "no cafe", regex = True)
    
    return merged


if __name__ == "__main__":    
    
    # write cleaned data to file
    with open("cleaned_data.csv", "w") as file:
        clean_data().to_csv(file, index = False)
