"""
Reads the RDA tables in database/dietary-requirements .csv files and compiles them into a single table saved as RDA.csv in database/clean-tables

ID      Age     Category    Sex     Calcium     Chromium        ...     water       carbohydrate    fibre       fat
1       0       infants     both    

"""

import pandas as pd
import string

rda_tables_directory = './dietary-requirements/'
rda_tables = [rda_tables_directory + table for table in ['elements.csv', 'vitamins.csv', 'water_and_macronutrients.csv']]

def cleanColumnTitle(title):

    new_name = title.lower()
    new_name_split = new_name.split()

    if new_name_split[0] == "vitamin":  # Set name to the vitamin type (e.g. 'vitamin c' --> 'c')
        new_name = new_name_split[1]
    elif new_name_split[1] == "equivalent":
        new_name = new_name_split[0]+"_"+new_name_split[1]
    elif new_name_split[0] == "pantothenic":
        new_name = "pantothenate"
    elif new_name_split[1] == "fiber":
        new_name = "fibre"
    elif new_name_split[1] == "water":
        new_name = "water"
    else:
        new_name = new_name_split[0]  # Else set to first word
    
    new_name = new_name.replace("-", "_")  # Replace odd characters with underscores so they're valid variable names
    new_name = new_name.replace("/", "_")

    return new_name

def cleanEntry(old_entry):

        new_entry = entry

        new_entry = new_entry.replace('â€f', '')
        new_entry = new_entry.replace('â€ƒ', '')
        new_entry = new_entry.replace('â€“', ' ')
        new_entry = new_entry.replace('–', ' ') # elements.csv has - between numbers
        new_entry = new_entry.replace('> ', '')

        new_entry = new_entry.split(' ')

        if new_entry[-1] == 'mo': # convert month to years

            if new_entry[0] == '7':
                new_entry[0] = '6'

            new_entry[0] = float(new_entry[0]) / 12
            new_entry[1] = float(new_entry[1]) / 12
            
        if len(new_entry) >= 2:
            new_entry = new_entry[0]
            new_entry = float(new_entry)
        else:
             new_entry = new_entry[0]
        
        return new_entry


first_row = ['Age', 'Category', 'Sex'] 

for file in rda_tables:
    df = pd.read_csv(file)
    nutrients_columns = df.columns[2:]

    for column in nutrients_columns:
        new_column_title = cleanColumnTitle(column)
        first_row.append(new_column_title) 

print(first_row)

# The new entries are identical for each table, so only need to perform it once
table_df = pd.read_csv(rda_tables[0])
old_entries = table_df.iloc[:, 1]
new_entries = []

for entry in old_entries:
    new_entry = cleanEntry(entry)
    new_entries.append(new_entry)
    
print(new_entries)

new_df = pd.DataFrame(columns=first_row)

for row_index, entry in enumerate(new_entries):
    if type(entry) == type(''):
        category = entry
    else:
        age = entry
        if category in ['Infants', 'Children']:
            sex = 'both'
        elif category in ['Males']:
            sex = 'male'
        elif category in ['Females', 'Pregnancy', 'Lactation']:
            sex = 'female'
        else: 
            print(f"ERROR: no category '{category}' detected")
            break

        new_row = [age, category, sex]

        for file in rda_tables:
            table_df = pd.read_csv(file)

            row = table_df.iloc[row_index, 2:]
            for nutrient_entry in row:
                clean_nutrient_entry = nutrient_entry
                for character in ['*'] + list(string.ascii_lowercase):
                    clean_nutrient_entry = clean_nutrient_entry.replace(character, '')
                if 'ND' in clean_nutrient_entry:
                    clean_nutrient_entry = None
                new_row.append(clean_nutrient_entry)

        new_df.loc[row_index] = new_row

print(new_df)

new_df.to_csv('./clean-tables/RDA.csv')