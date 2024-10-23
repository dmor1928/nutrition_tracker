"""
Reads the RDA tables in database/dietary-requirements .csv files and compiles them into a single table saved as RDA.csv in database/clean-tables

ID      Age     Category    Sex     Calcium     Chromium        ...     water       carbohydrate    fibre       fat
1       0       infants     both    200         0.2             ...     0.7         60              None        31
:
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
        if new_name == "a":
            new_name = "retinol"
    elif new_name_split[1] == "equivalent":
        new_name = new_name_split[0]+"_"+new_name_split[1]
    elif new_name_split[0] == "pantothenic":
        new_name = "pantothenate"
    elif new_name_split[1] == "fiber":
        new_name = "fibre"
    elif new_name_split[1] == "water":
        new_name = "water"
    elif new_name_split[0] == "linoleic":
        new_name = "n_6"
    elif new_name_split[0] == "alpha-linolenic":
        new_name = "n_3"
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


first_row = ['age', 'category', 'sex']  #The column titles
for file in rda_tables:
    df = pd.read_csv(file)
    nutrients_columns_titles = df.columns[2:]

    for title in nutrients_columns_titles:
        new_column_title = cleanColumnTitle(title)
        first_row.append(new_column_title) 

# Entries are identical on each table
table_df = pd.read_csv(rda_tables[0])
old_entries = table_df.iloc[:, 1]

new_entries = []

for entry in old_entries:
    new_entry = cleanEntry(entry)
    new_entries.append(new_entry)
    
# print(new_entries)

compiled_RDA_dataframe = pd.DataFrame(columns=first_row)

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

        compiled_RDA_dataframe.loc[row_index] = new_row


cofid_df = pd.read_csv('./clean-tables/complete_nutritional_data.csv')
cofid_nutrients = list(cofid_df.columns[2:])
rda_nutrients = list(compiled_RDA_dataframe.columns[3:])

# print("cofid: ", cofid_nutrients)
# print("rda   : ", rda_nutrients)
# for element in (set(cofid_nutrients) ^ set(rda_nutrients)):
#     print(element)
"""
Current assumptions/approximations: 
Vitamin K = K1 are the same
Total fibre = AOAC Fibre
vitamin A = retinol
Trans fat maximum daily intake = 0g for everyone

Data missing from complete_nutritional_data but included in RDA.csv:
chromium
choline
fluoride
molybdenum
water
k                           Just say k1 = k

Data missing from RDA.csv but included in complete_nutritional_data:
## Macros: ##
energy / calories (this can be chosen by the user?)
## Fat types: ##
trans                       Handled by missingFatRDAColumns
mono                        Will be handled by missingFatRDAColumns in future
satd                        Handled by missingFatRDAColumns
poly (polyunsaturated fat)  Will be handled by missingFatRDAColumns in future
cholesterol                 Handled by missingFatRDAColumns
## Vitamins: ##
niacin_equivalent           Just count as niacin
retinol_equivalent          Just count as retinol
k1                          Just say k1 = k
## Carotenes: ##
carotene
alpha_carotene
beta_carotene
lycopene
## Carotenoids: ##
lutein
## amino acids: ##
tryptophan_60
"""

def missingFatRDAColumns (age_column):
    # Add missing fat RDA to the 'fat' column
    total_fat_column = pd.Series()
    for row_index, age in enumerate(age_column):
        if age < 1:
            total_fat_column[row_index] = 30
        elif 1 <= age < 4:
            total_fat_column[ row_index] = 39
        else:
            total_fat_column[row_index] = 78

    saturated_fat_column = pd.Series()
    for row_index, age in enumerate(age_column):
        if age <= 1:
            saturated_fat_column[row_index] = None
        elif 1 < age <= 4:
            saturated_fat_column[row_index] = 10
        else:
            saturated_fat_column[row_index] = 20

    cholesterol_column = pd.Series()
    for row_index, age in enumerate(age_column):
        if age <= 1:
            cholesterol_column[row_index] = None
        else:
            cholesterol_column[row_index] = 300
    
    trans_fat_column = pd.Series()
    for row_index, age in enumerate(age_column):
        trans_fat_column[row_index] = 0
    
    return total_fat_column, saturated_fat_column, cholesterol_column, trans_fat_column

fat, satd, cholesterol, trans = missingFatRDAColumns(compiled_RDA_dataframe['age'])

compiled_RDA_dataframe = compiled_RDA_dataframe.assign(fat=fat.values)
compiled_RDA_dataframe = compiled_RDA_dataframe.assign(satd=satd.values)
compiled_RDA_dataframe = compiled_RDA_dataframe.assign(cholesterol=cholesterol.values)
compiled_RDA_dataframe = compiled_RDA_dataframe.assign(trans=trans.values)

macronutrient_percentages = pd.read_csv('./dietary-requirements/macronutrient_percentage_ranges.csv')

# print(macronutrient_percentages.columns)

for column_index, column_title in enumerate(list(macronutrient_percentages.columns)):
    column_entries = macronutrient_percentages[column_title]
    
    min_column = []
    max_column = []
    for index, entry in enumerate(column_entries):
        if '-' in entry:
            [entry_min, entry_max] = entry.split('-')
            min_column.append(float(entry_min))
            max_column.append(float(entry_max))
    
    macronutrient_percentages[column_title + '_min_percent'] = min_column
    macronutrient_percentages[column_title + '_max_percent'] = max_column

for column_title in ['fat', 'n_6', 'n_3', 'carbohydrate', 'protein']:
    macronutrient_percentages = macronutrient_percentages.drop(column_title, axis=1)

# print(macronutrient_percentages)

age_column = compiled_RDA_dataframe['age']
for column_title in list(macronutrient_percentages.columns):
    
    new_column = pd.Series()
    for row_index, age in enumerate(age_column):
        if age < 1:
            new_column[row_index] = None
        elif 1 <= age < 4:
            new_column[row_index] = macronutrient_percentages[column_title][0]
        elif 4 <= age < 18:
            new_column[row_index] = macronutrient_percentages[column_title][1]
        else:
            new_column[row_index] = macronutrient_percentages[column_title][2]
    
    compiled_RDA_dataframe = compiled_RDA_dataframe.assign(**{column_title: new_column.values})


# Changing 19, 31, and 51s in age category to 18, 30, 50
compiled_RDA_dataframe['age'] = compiled_RDA_dataframe['age'].replace([19.0], 18.0)
compiled_RDA_dataframe['age'] = compiled_RDA_dataframe['age'].replace([31.0], 30.0)
compiled_RDA_dataframe['age'] = compiled_RDA_dataframe['age'].replace([51.0], 50.0)

# print(compiled_RDA_dataframe)

# print(sorted(list(set(cofid_df.columns[2:]) & set(compiled_RDA_dataframe))))

# for item in sorted(compiled_RDA_dataframe.columns[3:]):
#     print(item)

sorted_list = ['age', 'category', 'sex'] + sorted(compiled_RDA_dataframe.columns[3:])
# print(sorted_list)

compiled_RDA_dataframe = compiled_RDA_dataframe[sorted_list]

compiled_RDA_dataframe.insert(0, 'id', [x for x in range(1, compiled_RDA_dataframe.shape[0]+1)])

compiled_RDA_dataframe = compiled_RDA_dataframe.replace(',', '', regex=True)

compiled_RDA_dataframe['chloride'] = compiled_RDA_dataframe['chloride'].apply(lambda x: float(x) * 1000)  # Convert g to mg

compiled_RDA_dataframe.to_csv('./clean-tables/RDA_defaults.csv', index=False)