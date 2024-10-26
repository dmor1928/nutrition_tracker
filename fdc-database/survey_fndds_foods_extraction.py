import numpy as np
from IPython.display import display
import pandas as pd

database_directory = "./FoodData_Central_csv_2024-04-18/"


foods = pd.read_csv(database_directory + "food.csv")
# print("foods data types: ", foods.data_type.unique())
# food.csv contains fdc_ids for ALL entries in database, whilst survey_fndds_food.csv contains fdc_ids for only
# the fndds foods
# BUT food.csv is the only one that contains that names of the food

# 1. Get each fdc_id of fndds_foods √

fndds_foods = pd.read_csv(database_directory + "survey_fndds_food.csv")


# 2. Print all fndds_foods containing 'almond' in name

fndds_food_names = foods.loc[foods['data_type'].isin(['survey_fndds_food', 'foundation_food'])]

fndds_containing_almond = fndds_food_names.loc[
    (fndds_food_names['description'].str.contains('almond', case=False)) & 
    (fndds_food_names['description'].str.contains('raw', case=False))]

print(fndds_containing_almond)
fdc_id = fndds_containing_almond['fdc_id'].iloc[0]
print(fdc_id)


# 3. Print nutritional information of raw almonds
nutrients = pd.read_csv(database_directory + "nutrient.csv")
nutrients.index = nutrients['id']
print(nutrients)

food_nutrients = pd.read_csv(database_directory + "food_nutrient.csv")

nutrient_ids = nutrients['id']
nutrient_names = nutrients['name']

raw_almonds_nutrients = food_nutrients.loc[food_nutrients['fdc_id'] == fdc_id][['nutrient_id', 'amount']]
raw_almonds_nutrients.index = raw_almonds_nutrients['nutrient_id']

print(raw_almonds_nutrients)

raw_almonds_nutritional_data = pd.concat([nutrients['name'], raw_almonds_nutrients['amount']], axis=1, keys=['name', 'amount'])

display(raw_almonds_nutritional_data.to_string())

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
