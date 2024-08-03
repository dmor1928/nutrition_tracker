import pandas as pd
import sqlite3

conn = sqlite3.connect('CoFID_2021_nutrition_information.db')

macros_data = pd.read_csv('databases/CoFID_2021_proximates.csv')[[
    'Food Name', 
    'Energy (kcal) (kcal)', 
    'Protein (g)', 
    'Fat (g)', 
    'Carbohydrate (g)', 
    'AOAC fibre (g)'
    ]]
macros_data.to_sql('macros', conn, if_exists='replace', index=False)

inorganics_data = pd.read_csv('databases/CoFID_2021_inorganics.csv')[[
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

inorganics_data.to_sql('inorganics', conn, if_exists='replace', index=False)

vitamins_data = pd.read_csv('database/CoFID_2021_vitamins.csv')[[
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

inorganics_data.to_sql('vitamisn', conn, if_exists='replace', index=False)

cur = conn.cursor()

for i, row in enumerate(cur.execute('SELECT * FROM macros')):
    print(row)
    if i > 20:
        break

conn.close()
