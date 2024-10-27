import pandas as pd

database_directory = "./FoodData_Central_csv_2024-04-18/"

foods = pd.read_csv(database_directory + "food.csv")

print("foods data types: ", foods.data_type.unique())


sr_legacy_food_names = foods.loc[foods['data_type'] == 'sr_legacy_food']
sr_legacy_foods = pd.read_csv(database_directory + "sr_legacy_food.csv")

# SR Legacy Foods
# Columns: fdc_id   NDB_number

# 1. Get each fdc_id of SR Legacy foods
# 2. Print all fdc_ids of SR Legacy Food containing 'almond' in name
# 3. Print nutritional information of raw almonds

nutrients = pd.read_csv(database_directory + "nutrient.csv")

nutrients_niacin_row = nutrients.loc[nutrients['name'] == 'niacin']
print("nutrients_niacin_row: ", nutrients_niacin_row)
niacin_id = nutrients.loc[nutrients['name'] == 'Niacin']['id'].iloc[0]

print("niacin_id: ", niacin_id)

food_nutrients = pd.read_csv(database_directory + "food_nutrient.csv")

sr_legacy_food_nutrients = food_nutrients.loc[food_nutrients['fdc_id'].isin(sr_legacy_foods['fdc_id'])]

# print(sr_legacy_food_nutrients.nutrient_id.unique())

sr_legacy_foods_niacin_values = sr_legacy_food_nutrients.loc[sr_legacy_food_nutrients['nutrient_id'] == niacin_id]
print(sr_legacy_foods_niacin_values)
