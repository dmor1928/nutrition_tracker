import pandas as pd

database_directory = "./FoodData_Central_csv_2024-04-18/"

nutrients = pd.read_csv(database_directory + "nutrient.csv")

nutrients_list = []
for nutrient_name in nutrients['name']:
    nutrients_list.append(nutrient_name)

print(nutrients_list)

water = ['water']

carbohydrates = [ 'total carbohydrates', 'fiber', 'sugar', 'added sugar']
# Soluble and insoluble fiber?

carbohydrate_monosaccharides = ['glucose', 'fructose', 'galactose']
carbohydrate_polysaccharides = ['starch', 'glycogen']

fats = ['total_fat', 'monounsaturated fat', 'polyunsaturated fat', 'omega-3 ALA', 
        'omega-3 EPA/DHA', 'omega-6', 'saturated fat', 'cholesterol']

protein = ['protein']

amino_acids = ['phenylalanine', 'valine', 'threonine', 'tryptophan', 'methionine', 'leucine', 
               'isoleucine', 'lysine', 'histidine']
# conditionally esssential amino acids for children?

# phenylalanine and tyrosine can be synthesised from the other using the enzyme 
# phenylalanine/tyrosine ammonia-lyase
# Methionine and cysteine are grouped together because one of them can be synthesized from 
# the other using the enzyme methionine S-methyltransferase and the catalyst methionine synthase

vitamins = [['B1', 'thiamin'], ['B2', 'riboflavin'], ['B3', 'niacin'], ['B5', 'pantothenate'], 
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

phytochemicals = ['lypocene', 'lutein and zeaxanthin', 'quarcetin', 'flavonoids', 'resveratrol', 
                  'myricetin']
# Others: Isoflavones, Pro-anthocyanidins, Purines


#The World Health Organization recommends that added sugars should represent no 
# more than 10% of total energy intake

# nine kilocalories in each gram of fat. 

# CoQ 10?
# Beta alanine
