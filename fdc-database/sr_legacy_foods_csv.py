import pandas as pd

database_directory = "./FoodData_Central_csv_2024-04-18/"

fndds_ingredient_nutrient_value = pd.read_csv(database_directory + "/sr_legacy_food.csv")

foods_sr_legacy_only = pd.read_csv(database_directory + "food.csv")
foods_sr_legacy_only = foods_sr_legacy_only.loc[foods_sr_legacy_only['fdc_id'].isin(fndds_ingredient_nutrient_value.fdc_id)]
foods_sr_legacy_only = foods_sr_legacy_only.drop(['data_type', 'publication_date'], axis=1)
foods_sr_legacy_only = foods_sr_legacy_only.rename(columns={'description': 'name'})

foods_sr_legacy_only.to_csv('fdc-reduced/sr_legacy_food.csv', index=False)

print(foods_sr_legacy_only.name.str.len().max())

print(foods_sr_legacy_only)