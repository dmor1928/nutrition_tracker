"""
Script for making copy of foods.csv but without branded food, which makes up 97% of the database.
The branded food only has limited nutritional information.

The reduced foods database will only contain:
sr_legacy_food
survey_fndds_food

UPDATE 27/10/24:
sr_legacy doesn't have food category, therefore we will only be usinv survey_fndds_food

"""
import numpy as np
from IPython.display import display
import pandas as pd

database_directory = "./FoodData_Central_csv_2024-04-18/"

reduced_databases_directory = './fdc-reduced/'

# Reducing foods
foods = pd.read_csv(database_directory + "food.csv")
print("foods data types: ", foods.data_type.unique())
reduced_foods = foods.loc[foods['data_type'].isin(['survey_fndds_food'])] 
reduced_foods = reduced_foods.drop(['data_type', 'publication_date'], axis=1)
reduced_foods.rename(columns={'description':'name'}, inplace=True)
reduced_foods.to_csv(reduced_databases_directory + 'food.csv', index=False)

# # Reducing food_nutrients
food_nutrients = pd.read_csv(database_directory + "food_nutrient.csv")
reduced_food_nutrients = food_nutrients[food_nutrients['fdc_id'].isin(reduced_foods['fdc_id'])]
reduced_food_nutrients = reduced_food_nutrients.drop(['id','data_points', 'derivation_id', 'min', 'max', 'median', 'loq', 'footnote', 'min_year_acquired', 'percent_daily_value'], axis=1)
reduced_food_nutrients.index.name = 'id'
reduced_food_nutrients.to_csv(reduced_databases_directory + 'food_nutrient.csv')

# Reducing food_portion
food_portions = pd.read_csv(database_directory + 'food_portion.csv')
reduced_food_portions = food_portions.loc[food_portions['fdc_id'].isin(reduced_foods['fdc_id'])]
reduced_food_portions = reduced_food_portions.drop(['data_points', 'footnote', 'min_year_acquired'], axis=1)
reduced_food_portions.index.name = 'id'
reduced_food_portions.to_csv(reduced_databases_directory + 'food_portion.csv')

# TO-DO: Reducing nutrients to relevant nutrients
nutrients = pd.read_csv(database_directory + 'nutrient.csv')
nutrients = nutrients.drop(['nutrient_nbr', 'rank'], axis=1)
nutrients.to_csv(reduced_databases_directory + 'nutrient.csv', index=False)


# This does not work, because sr_legacy and suvery_fndds foods do not have portion data

# food.csv contains fdc_ids for ALL entries in database, whilst survey_fndds_food.csv contains fdc_ids for only
# the fndds foods
# BUT food.csv is the only one that contains that names of the food

# 1. Get each fdc_id of fndds_foods √

# fndds_foods = pd.read_csv(database_directory + "survey_fndds_food.csv")


# 2. Print all fndds_foods containing 'almond' in name


def getNutrientID(nutrient_name, nutrients_database):
    nutrient_row = nutrients_database.loc[nutrients_database['name'] == nutrient_name]
    nutrient_id = nutrient_row['id'].iloc[0]
    # print(f"nutrients_database {nutrient_name} row: ", nutrient_row)
    return nutrient_id


# nutrients_niacin_row = nutrients.loc[nutrients['name'] == 'niacin']
# print("nutrients_niacin_row: ", nutrients_niacin_row)
# niacin_id = nutrients.loc[nutrients['name'] == 'niacin']['id'].iloc[0]
# print("niacin_id: ", niacin_id)

# food_nutrients = pd.read_csv(database_directory + "food_nutrient.csv")

# sr_legacy_food_nutrients = food_nutrients.loc[food_nutrients['fdc_id'].isin(sr_legacy_foods['fdc_id'])]

# # print(sr_legacy_food_nutrients.nutrient_id.unique())

# sr_legacy_foods_niacin_values = sr_legacy_food_nutrients.loc[sr_legacy_food_nutrients['nutrient_id'] == niacin_id]
# print(sr_legacy_foods_niacin_values)
