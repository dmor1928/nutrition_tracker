""" 
 -  Reads the CoFID.csv files and returns two cleaned .csv files in ./clean-tables
        1. A table showing the relevant nutritional information for all food 
            entries
        2. A table of the units that each nutrient is recorded in
 -  Both in .csv tables, ready to be imported as sql databases in csv-to-sqlalchemy.py
 -  Extracts the information from multiple .csv files, (proximates, inorganics, vitamins)
    and compiles them into a single .db file named 'CoFID_2021_nutrition_information' 
 -  All nutrtional information is given per 100g of food item
"""

import pandas as pd
# import sqlite3
import os

# database_name = 'CoFID_2021_nutrition_information.db'
# conn = sqlite3.connect(database_name)

proximates_data = pd.read_csv('CoFID/CoFID_2021_proximates.csv', skiprows=[1, 2])[[
    'Food Name', 
    'Energy (kcal) (kcal)', 
    'Protein (g)', 
    'Fat (g)', 
    'Carbohydrate (g)', 
    'AOAC fibre (g)',
    'Satd FA /100g fd (g)',
    'n-6 poly /100g food (g)',
    'n-3 poly /100g food (g)',
    'Mono FA /100g food (g)',
    'Poly FA /100g food (g)',
    'Trans FAs /100g food (g)',
    'Cholesterol (mg)'
    ]]

# proximates_data.to_sql('proximates', conn, if_exists='replace', index=False)
# Printing the first 10 items as an example
# print("PROXIMATES:")
# for i, row in enumerate(cur.execute('SELECT * FROM proximates')):
#     print(row)
#     if i > 10:
#         break

inorganics_data = pd.read_csv('CoFID/CoFID_2021_inorganics.csv', skiprows=[1, 2])[[
    'Sodium (mg)', 
    'Potassium (mg)', 
    'Calcium (mg)', 
    'Magnesium (mg)', 
    'Phosphorus (mg)', 
    'Iron (mg)', 
    'Copper (mg)', 
    'Zinc (mg)', 
    'Chloride (mg)', 
    'Manganese (mg)', 
    'Selenium (µg)', 
    'Iodine (µg)'
    ]]

# inorganics_data.to_sql('inorganics', conn, if_exists='replace', index=False)

vitamins_data = pd.read_csv('CoFID/CoFID_2021_vitamins.csv', skiprows=[1, 2])[[
    'Retinol (µg)', 
    'Carotene (µg)', 
    'Retinol Equivalent (µg)', 
    'Vitamin D (µg)', 
    'Vitamin E (mg)', 
    'Vitamin K1 (µg)', 
    'Thiamin (mg)', 
    'Riboflavin (mg)', 
    'Niacin (mg)', 
    'Tryptophan/60 (mg)', 
    'Niacin equivalent (mg)', 
    'Vitamin B6 (mg)', 
    'Vitamin B12 (µg)', 
    'Folate (µg)', 
    'Pantothenate (mg)', 
    'Biotin (µg)', 
    'Vitamin C (mg)'
    ]]

# vitamins_data.to_sql('vitamins', conn, if_exists='replace', index=False)

vitamin_fractions_data = pd.read_csv('CoFID/CoFID_2021_vitamin_fractions.csv', skiprows=[1, 2])[[
    'Alpha-carotene (µg)', 
    'Beta-carotene (µg)',
    'Lutein (µg)', 
    'Lycopene (µg)'
]]

# vitamin_fractions_data.to_sql('vitamin_fractions', conn, if_exists='replace', index=False)

complete_nutritional_data = pd.concat([proximates_data, inorganics_data, vitamins_data, vitamin_fractions_data], axis=1)

column_names = list(complete_nutritional_data.columns)
new_names = [None] * len(column_names)
units = [None] * len(column_names)
for n, column_name in enumerate(column_names):
    # Extracting unit from original column name
    if "(" in column_name:
        units[n] = column_name.split("(")[1].split(")")[0]
    else:
        units[n] = None  # 'Food name' does not have unit so must account for that

    new_name = column_name.lower()  # For consistent naming convention
    new_name_split = new_name.split()

    if new_name_split[0] == "vitamin":  # Set name to the vitamin type (e.g. 'vitamin c' --> 'c')
        new_name = new_name_split[1]
    elif new_name_split[0] == "food":
        new_name = "name"
    elif new_name_split[1] == "equivalent":
        new_name = new_name_split[0]+"_"+new_name_split[1]
    elif new_name_split[1] == "fibre":
        new_name = "fibre"
    else:
        new_name = new_name_split[0]  # Else set to first word
    
    new_name = new_name.replace("-", "_")  # Replace odd characters with underscores so they're valid variable names
    new_name = new_name.replace("/", "_")

    new_names[n] = new_name

print("The new nutrient names: ", new_names)
print("The units: ", units)

complete_nutritional_data.columns = new_names
complete_nutritional_data.insert(0, 'id', range(1, len(complete_nutritional_data)+1)) # Add id column at front for primary key

nutrients_units = pd.concat([pd.Series(new_names, name="nutrients"), pd.Series(units, name="unit")], axis=1)
nutrients_units.insert(0, 'nutrient_id', range(1, len(nutrients_units)+1)) # Add id column at front for primary key

sorted_list = ['id', 'name'] + sorted(complete_nutritional_data.columns[2:])
print(sorted_list)

complete_nutritional_data = complete_nutritional_data[sorted_list]

outdir = './clean-tables'
if not os.path.exists(outdir):
    os.mkdir(outdir)

complete_nutritional_data.to_csv(outdir + '/complete_nutritional_data.csv', index=False)
nutrients_units.to_csv(outdir + '/nutrients_units.csv', index=False)


# nutrients_units.to_sql('nutrients_units', conn, if_exists='replace', index=False)
# complete_nutritional_data.to_sql('complete_nutritional_data', conn, if_exists='replace', index=False)
# conn.close()

# Adding primary key ID_column to complete_nutritonal_data

print(f'Nutritional information successfully extracted to {outdir}/nutrients_units.csv')