# Author: Leslie Huang (lh1036)
# Description: This program imports raw data files 
# (#1: Restaurant Grades Data, #2: Sidewalk Cafe Data), 
# implements data cleaning, and saves the cleaned and merged file.
#
# I have written all non-trivial data cleaning as functions to allow for 
# unit testing. However, data cleaning is specific to the messiness of the data; however, 
# I do not write functions or unittests for the execution of simple Pandas methods, 
# for example drop_duplicate.

import pandas as pd
import re

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

if __name__ == "__main__":

    ### read in (1) Restaurant Inspection Dataset downloaded from  https://data.cityofnewyork.us/Health/DOHMH-New-York-City-Restaurant-Inspection-Results/xx67-kt59
    # PLEASE NOTE: The online version is regularly updated. I use the 11/27/16 version.
    restaurant_grades = pd.read_csv("DOHMH_New_York_City_Restaurant_Inspection_Results.csv", dtype = str, keep_default_na = False, na_values = [])
    
    ### Because of the size of the dataset, processing time of this data is nontrivial. 
    # Thus, I proceed in the following steps:
    # (1) Fixing names and formatting, so that references are consistent
    # (2) drop rows and columns that won't be used, to reduce the size of the DF that undergoes cleaning
    # (3) clean remaining DF
    
    ### (1) Fixing the names
    restaurant_grades = clean_colnames(restaurant_grades)
    restaurant_grades = restaurant_grades.rename(columns = {"dba": "restaurant"})
    restaurant_grades = strip_whitespace(restaurant_grades, ["street", "restaurant"])
    
    ### (2) Dropping
    
    # drop unneeded columns
    restaurant_grades = restaurant_grades.drop(["recorddate", "camis", "action", "phone", "violationcode"], axis = 1)
    
    # drop rows:
    restaurant_grades = restaurant_grades.drop_duplicates()

    # drop observations missing essential information:
    # (a) name, category, street address or (b) both score and grade
    restaurant_grades = drop_multiple_column_nulls(restaurant_grades, ["restaurant", "street", "cuisinedescription"])
    restaurant_grades = restaurant_grades[pd.notnull(restaurant_grades["score"]) | pd.notnull(restaurant_grades["grade"])]
    
    # drop observations with negative scores (data entry error)
    restaurant_grades = restaurant_grades.loc[pd.to_numeric(restaurant_grades["score"], errors = "ignore") >= 0]
    
    ### (3) Cleanup
    
    # clean up whitespace and lowercase entire DF
    restaurant_grades = convert_lowercase(restaurant_grades)
    
    # create unique ID var from address
    restaurant_grades = concat_cols(restaurant_grades, ["building", "street", "zipcode"], "address_id")
    
    # set first-listed cuisine as the primary cuisine
    restaurant_grades = make_primary_cuisine(restaurant_grades, "cuisinedescription", "cuisine_primary")
      
      
    ### Read in (2) Sidewalk Cafe Dataset, downloaded from
    # https://data.cityofnewyork.us/Business/Sidewalk-Caf-Licenses-and-Applications/qcdj-rwhu
    # I use the 12/2/2016 version.
    
    sidewalk_licenses = pd.read_csv("Sidewalk_Caf__Licenses_and_Applications.csv", dtype = str, keep_default_na = False, na_values = [])

    # lowercase and strip whitespace
    sidewalk_licenses = clean_colnames(sidewalk_licenses)
    sidewalk_licenses = convert_lowercase(sidewalk_licenses)
    sidewalk_licenses = strip_whitespace(sidewalk_licenses, ["street", "business_name", "business_name2"])

    # create unique ID var from address
    sidewalk_licenses = concat_cols(sidewalk_licenses, ["building", "street", "zip"], "address_id")

    # Keep only needed columns
    # Note: I drop "building", "street", "zip" AFTER using them to construct address_id
    sidewalk_licenses = sidewalk_licenses[["license_nbr", "lic_status", "city", "issuance", "business_name", "business_name2", "issuance_dd", "address_id"]]


### Merge and output the merged file

    # merge on unique address_id var
    merged = pd.merge(restaurant_grades, sidewalk_licenses, left_on = "address_id", right_on = "address_id", how = "left")

    # write cleaned data to file
    with open("cleaned_data.csv", "w") as file:
        merged.to_csv(file)