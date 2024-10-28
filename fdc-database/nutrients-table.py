import pandas as pd

database_directory = "./FoodData_Central_csv_2024-04-18/"

nutrients = pd.read_csv(database_directory + "nutrient.csv")

energy = ['energy']

water = ['water']

carbohydrates = [ 'carbohydrate', 'fiber', 'sugar', 'sugars, added']
# Soluble and insoluble fiber?

carbohydrate_monosaccharides = ['glucose', 'fructose', 'galactose']
carbohydrate_polysaccharides = ['starch', 'glycogen']

fats = ['fat', 'monounsaturated', 'polyunsaturated', 'ALA', 
        'EPA', 'DHA', 'n-6', 'saturated', 'cholesterol', ' trans']

protein = ['protein']

amino_acids = ['phenylalanine', 'valine', 'threonine', 'tryptophan', 'methionine', 'leucine', 
               'isoleucine', 'lysine', 'histidine']
# conditionally esssential amino acids for children?

# phenylalanine and tyrosine can be synthesised from the other using the enzyme 
# phenylalanine/tyrosine ammonia-lyase
# Methionine and cysteine are grouped together because one of them can be synthesized from 
# the other using the enzyme methionine S-methyltransferase and the catalyst methionine synthase

vitamins = ['thiamin', 'riboflavin', 'niacin', 'pantothenate', 'B-6', 'B-12', 'choline', 'biotin', 
              'folate', 'Vitamin A', 'retinol', 'Vitamin C', 'Vitamin D', 'Vitamin E', 'Vitamin K']

vitamins_easier_naming_for_html = [['B1', 'thiamin'], ['B2', 'riboflavin'], ['B3', 'niacin'], ['B5', 'pantothenate'], 
              ['B6', 'b6'], ['B12', 'b12'], ['Choline', 'choline'], ['Biotin', 'biotin'], 
              ['Folate', 'folate'], ['Vitamin A', 'retinol'], ['Vitamin C', 'c'], 
              ['Vitamin D', 'd'], ['Vitamin E', 'e'], ['Vitamin K', 'k']]
# The Food and Nutrition Board of the Institute of Medicine has established 
# Tolerable Upper Intake Levels (ULs) for seven vitamins
# https://www.ncbi.nlm.nih.gov/books/NBK56068/table/summarytables.t7/?report=objectonly

macrominerals = ['calcium', 'chloride', 'magnesium', 'phosphorus', 'potassium', 'sodium', 'sulfur']
traceminerals = ['chromium', 'copper', 'iodine', 'iron', 'manganese', 'molybdenum', 'selenium', 'zinc' ]
ultratrace = ['Bromine', 'Arsenic', 'Nickel', 'Fluorine', 'Boron', 'Lithium', 'Strontium', 'Silicon', 'Vanadium']
# Ultratrace: unconfirmed and unproven for human health but may be requireed in extremely small doses
# Tolerable Upper Intake Levels for minerals, from the European Food Safety Agency (EFSE)
# https://www.efsa.europa.eu/sites/default/files/2024-05/ul-summary-report.pdf
# Tolerable Uppr Intake Levels for minerals (elements) from Food and Nutrition Board (USA)
# https://www.ncbi.nlm.nih.gov/books/NBK545442/table/appJ_tab9/?report=objectonly

phytochemicals = ['lycopene', 'lutein + zeaxanthin', 'quercetin', 'flavonoids', 'resveratrol', 
                  'myricetin']
# Others: Isoflavones, Pro-anthocyanidins, Purines


#The World Health Organization recommends that added sugars should represent no 
# more than 10% of total energy intake

# nine kilocalories in each gram of fat. 

# CoQ 10?
# Beta alanine


nutrients_to_display = {}

for category in [energy, water, carbohydrates, fats, protein, amino_acids, vitamins, 
                 macrominerals, traceminerals, ultratrace, phytochemicals]:
    nutrient_category = {}
    for nutrient in category:
        filtered_row = nutrients[nutrients['name'].str.contains(nutrient, case=False, na=False)][['id', 'name']].values.tolist()
        matching_names = []
        for row in filtered_row:
            matching_names.append(row)
        nutrient_category[nutrient] = matching_names
    nutrients_to_display[f'{category}'] = nutrient_category


import json

print(json.dumps(nutrients_to_display, indent=4))

out_file = open("matching_nutrients.json", "w")

json.dump(nutrients_to_display, out_file, indent=4)
