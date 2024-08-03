import pandas as pd
import sqlite3

conn = sqlite3.connect('CoFID_2021_nutrition_information.db')

proximates_data = pd.read_csv('database/CoFID_2021_proximates.csv')[[
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
proximates_data.to_sql('proximates', conn, if_exists='replace', index=False)

inorganics_data = pd.read_csv('database/CoFID_2021_inorganics.csv')[[
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
vitamins_data.to_sql('inorganics', conn, if_exists='replace', index=False)


vitamin_fractions_data = pd.read_csv('database/CoFID_2021_vitamin_fractions.csv')[[
    'Alpha-carotene (µg)', 
    'Beta-carotene (µg)',
    'Lutein (µg)', 
    'Lycopene (µg)'
]]
vitamin_fractions_data.to_sql('vitamin_fractions', conn, if_exists='replace', index=False)

cur = conn.cursor()

for i, row in enumerate(cur.execute('SELECT * FROM proximates')):
    print(row)
    if i > 20:
        break

conn.close()
