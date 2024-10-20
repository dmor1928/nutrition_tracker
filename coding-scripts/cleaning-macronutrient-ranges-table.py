import pandas as pd

macronutrient_percentages = pd.read_csv('./dietary-requirements/acceptable_macronutrient_distribution_ranges.csv').T

print(macronutrient_percentages)

macronutrient_percentages = macronutrient_percentages.iloc[1:, 1:]

def cleanEntriesMacroPercentages(entry):
    new_entry = str(entry)

    new_entry = new_entry.lower()
    new_entry = new_entry.replace('â€f', '')
    new_entry = new_entry.replace('â€ƒ', '')
    new_entry = new_entry.replace('â€“', '-')
    new_entry = new_entry.replace('–', ' ') # elements.csv has - between numbers
    new_entry = new_entry.replace('> ', '')

    if new_entry[:2] == 'n-':
        new_entry = 'n_' + new_entry[2]

    return new_entry

macronutrient_percentages = macronutrient_percentages.map(cleanEntriesMacroPercentages)

macronutrient_percentages.to_csv('./dietary-requirements/macronutrient_percentage_ranges.csv')

print(macronutrient_percentages)
