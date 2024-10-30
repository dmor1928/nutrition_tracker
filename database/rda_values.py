import pandas as pd

def getOrganisedAminoAcidRDAs(csv_directory):
    rda_amino_acids = pd.read_csv(csv_directory)
    # rda_amino_acids has units mg per kg bodyweight
    reorganised_rda_amino_acids = rda_amino_acids.melt(
        id_vars=['rda_profile_id'], 
        value_vars=list(rda_amino_acids.columns[1:]), var_name='nutrient_name')
    reorganised_rda_amino_acids['unit'] = 'mg_per_kg'

    return reorganised_rda_amino_acids

def getOrganisedVitaminMineralMacroRDAs(csv_directory):
    rda_vit_min_macros = pd.read_csv(csv_directory)
    reorganised_rda_vit_min_macros = rda_vit_min_macros.melt(
        id_vars=['rda_profile_id'],
        value_vars=list(rda_vit_min_macros.columns[1:]), var_name='nutrient_name'
    )
    reorganised_rda_vit_min_macros = reorganised_rda_vit_min_macros.sort_values('rda_profile_id')

    g_nutrients = ['chlorine', 'carbohydrate_total', 'total_dietary_fibre', 'total_fat', 'total_saturated_fat', 
                   'trans_fat', 'omega_6', 'omega_3', 'total_protein']
    mg_nutrients = ['calcium', 'fluoride', 'iron', 'magnesium', 'manganese', 'phosphorus', 'zinc', 
                    'potassium', 'sodium', 'vit_c', 'vit_e', 'thiamin', 'riboflavin', 'niacin', 'b6', 
                    'pantothenic_acid', 'choline', 'cholesterol']
    ug_nutrients = ['chromium', 'copper', 'iodine', 'molybdenum', 'selenium', 'vit_a', 'vit_d', 'vit_k', 
                    'folate', 'b12', 'biotin']
    litre_nutrients = ['water']
    percent_nutrients = ['carbohydrate_max_percent', 'carbohydrate_min_percent', 'fat_max_percent', 
                         'fat_min_percent', 'omega_3_max_percent', 'omega_3_min_percent',
                         'omega_6_max_percent',	'omega_6_min_percent', 'protein_max_percent', 'protein_min_percent',
                         ]
    
    reorganised_rda_vit_min_macros['unit'] = "NA"
    reorganised_rda_vit_min_macros.loc[reorganised_rda_vit_min_macros['nutrient_name'].isin(g_nutrients), 'unit'] = 'g'
    reorganised_rda_vit_min_macros.loc[reorganised_rda_vit_min_macros['nutrient_name'].isin(mg_nutrients), 'unit'] = 'mg'
    reorganised_rda_vit_min_macros.loc[reorganised_rda_vit_min_macros['nutrient_name'].isin(ug_nutrients), 'unit'] = 'μg'
    reorganised_rda_vit_min_macros.loc[reorganised_rda_vit_min_macros['nutrient_name'].isin(litre_nutrients), 'unit'] = 'ml'
    reorganised_rda_vit_min_macros.loc[reorganised_rda_vit_min_macros['nutrient_name'].isin(percent_nutrients), 'unit'] = 'percent'

    for index, row in reorganised_rda_vit_min_macros.iterrows(): # Ensuring water is in ml and not L
        if row['nutrient_name'] == "water":
            reorganised_rda_vit_min_macros.loc[index, 'value'] = row['value'] * 1000
            print("done")

    if not reorganised_rda_vit_min_macros.loc[reorganised_rda_vit_min_macros['unit'] == "NA"].empty:
        print("Error: some nutrients in reorganised_rda_vit_min_macros contains undefined units")
        print(reorganised_rda_vit_min_macros.loc[reorganised_rda_vit_min_macros["unit"] == "NA"])

    return reorganised_rda_vit_min_macros

rda_vit_min_macros = getOrganisedVitaminMineralMacroRDAs('./clean-tables/rda-csv/rda_vit_min_macros.csv')
rda_amino_acids = getOrganisedAminoAcidRDAs('./clean-tables/rda-csv/rda_amino_acids.csv')

rda_values = pd.concat([rda_vit_min_macros, rda_amino_acids])
rda_values = rda_values.sort_values(by=['rda_profile_id', 'nutrient_name'])
rda_values = rda_values.reset_index(drop=True)
rda_values.index.name = 'id'

print(rda_values)

rda_values.to_csv('./clean-tables/rda-values/rda_values.csv')

#Weird whitespace glitch. Whitespace was being adding to the methione_and_cysteine cells.. Very bizarre.
# first get all lines from file
with open('./clean-tables/rda-values/rda_values.csv', 'r') as f:
    lines = f.readlines()

# remove spaces
lines = [line.replace(' ', '') for line in lines]

# finally, write lines in the file
with open('./clean-tables/rda-values/rda_values.csv', 'w') as f:
    f.writelines(lines)