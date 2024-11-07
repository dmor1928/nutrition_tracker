import pandas as pd

database_directory = "./FoodData_Central_csv_2024-04-18/"

fndds_ingredient_nutrient_value = pd.read_csv(database_directory + "/sr_legacy_food.csv")

foods_sr_legacy_only = pd.read_csv(database_directory + "food.csv")
foods_sr_legacy_only = foods_sr_legacy_only.loc[foods_sr_legacy_only['fdc_id'].isin(fndds_ingredient_nutrient_value.fdc_id.values)]
foods_sr_legacy_only = foods_sr_legacy_only.drop(['data_type', 'publication_date'], axis=1)
foods_sr_legacy_only = foods_sr_legacy_only.rename(columns={'description': 'name'})

food_nutrient = pd.read_csv(database_directory + "/food_nutrient.csv")
sr_legacy_food_nutrient = food_nutrient.loc[food_nutrient['fdc_id'].isin(foods_sr_legacy_only['fdc_id'].values)]
sr_legacy_food_nutrient = sr_legacy_food_nutrient.drop(['id','data_points', 'derivation_id', 'min', 'max', 'median', 'loq', 'footnote', 'min_year_acquired', 'percent_daily_value'], axis=1)

sr_legacy_food_nutrient.index.name = 'id'

sr_legacy_food_nutrient.to_csv('fdc-reduced/sr_legacy_food_nutrient.csv')

print(foods_sr_legacy_only.name.str.len().max())

print(foods_sr_legacy_only)
print(sr_legacy_food_nutrient)