import pandas as pd

chosen_matching_nutrients = pd.read_json('chosen_matching_nutrients.json')

# print(chosen_matching_nutrients)

# print(chosen_matching_nutrients.Energy)
# just_energy = chosen_matching_nutrients.Energy

# print(just_energy.iloc[0])

for nutrient in chosen_matching_nutrients.columns:
    nutrient_measurements = chosen_matching_nutrients[nutrient].iloc[0]
    print(nutrient_measurements)
    break