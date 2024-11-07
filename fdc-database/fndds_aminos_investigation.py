import pandas as pd
import numpy as np

database_directory = "./FoodData_Central_csv_2024-04-18/"

reduced_databases_directory = './fdc-reduced/'

amino_acids = {"phenylalanine": 1217,
                "tyrosine": 1218,
                "valine": 1219,
                "threonine": 1211,
                "tryptophan": 1210,
                "methionine": 1215,
                "cysteine": 1232,  # Empty
                "leucine": 1213,
                "isoleucine": 1212,
                "lysine": 1214,
                "histidine": 1221,}

# Reducing foods

# foods = pd.read_csv(database_directory + "food.csv")
# print("foods data types: ", foods.data_type.unique())

# reduced_foods = foods.loc[foods['data_type'].isin(['sr_legacy_food'])] 
# reduced_foods = reduced_foods.drop(['data_type', 'publication_date'], axis=1)
# reduced_foods.rename(columns={'description':'name'}, inplace=True)

sr_legacy_food = pd.read_csv(database_directory + "sr_legacy_food.csv")
# sr_legacy has fdc_id and ndb_number

foundation_food = pd.read_csv(database_directory + "foundation_food.csv")
# foundation_food has fdc_id and ndb_number and footnote

fndds_ingredient_nutrient_value = pd.read_csv(database_directory + "fndds_ingredient_nutrient_value.csv")
# has ingredient_code, Ingredient_description, nutrient_code, nutrient_value, nutrient_value_source, fdc_id, derivation_code, sr_addmod_year foundation_year_acquired start_date end_date

nutrient = pd.read_csv(database_directory + 'nutrient.csv')
# has id, name, unit_name, nutrient_nbr, rank
# unit_name is just the name of the standard unit of measure of nutrient per 100g of food, e.g. g, mg, kcal

nutrient['nutrient_nbr'] = nutrient['nutrient_nbr']

nutrient_nbr_to_name = pd.Series(nutrient.name.values, index=nutrient.nutrient_nbr).to_dict()
nutrient_nbr_to_id = pd.Series(nutrient.id.values, index=nutrient.nutrient_nbr).to_dict()

fndds_ingredient_nutrient_value['Nutrient name'] = fndds_ingredient_nutrient_value['Nutrient code'].apply(lambda x: nutrient_nbr_to_name.get(x))
fndds_ingredient_nutrient_value['nutrient_id'] = fndds_ingredient_nutrient_value['Nutrient code'].apply(lambda x: nutrient_nbr_to_id.get(x))
fndds_ingredient_nutrient_value = fndds_ingredient_nutrient_value.drop(['Foundation year acquired','Start date', 'End date', 'SR AddMod year', 'Derivation code'], axis=1)

print("fndds_ingredient_nutrient_value: ")
print(fndds_ingredient_nutrient_value)

print("Nutrient value sources: ")
print(fndds_ingredient_nutrient_value['Nutrient value source'].unique())


import json
file = open('clean_fdc_nutrients_dictionary.json')
nutrient_reduced_ids = pd.Series(json.load(file))
print(nutrient_reduced_ids)

nutrient_id_to_number = pd.Series(nutrient.nutrient_nbr.values, index=nutrient.id).to_dict()

nutrient_reduced_numbers = nutrient_reduced_ids.apply(lambda x: nutrient_id_to_number.get(x))

fndds_ingredient_nutrient_value = fndds_ingredient_nutrient_value.loc[fndds_ingredient_nutrient_value['Nutrient code'].isin(nutrient_reduced_numbers.values)]

# Removing 'Nutrient as ingredient' entries
fndds_ingredient_nutrient_value = fndds_ingredient_nutrient_value.loc[fndds_ingredient_nutrient_value['Nutrient value source'] != "Nutrient as ingredient"]

print("fndds_ingredient_nutrient_value after filtering:")

print(fndds_ingredient_nutrient_value)

# fndds_ingredient_nutrient_value = fndds_ingredient_nutrient_value.rename(columns={'Nutrient value': 'amount', 'FDC ID': 'fdc_id'})
# fndds_ingredient_nutrient_value.index.name = 'id'

# fndds_ingredient_nutrient_value = fndds_ingredient_nutrient_value.drop(fndds_ingredient_nutrient_value.loc[fndds_ingredient_nutrient_value['fdc_id'].isin([0, np.nan])].index)

# fndds_ingredient_nutrient_value[['fdc_id', 'nutrient_id', 'amount']].to_csv('fdc-reduced/sr_legacy_food_nutrient.csv')