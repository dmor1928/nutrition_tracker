import pandas as pd
import glob, os

FOOD_AND_NUTRITION_BOARD_DIETARY_REFERENCE_INTAKES = [
    ELEMENTS := 'https://www.ncbi.nlm.nih.gov/books/NBK545442/table/appJ_tab3/?report=objectonly',
    WATER_AND_MACRONUTRIENTS := 'https://www.ncbi.nlm.nih.gov/books/NBK56068/table/summarytables.t4/?report=objectonly',
    VITAMINS := 'https://www.ncbi.nlm.nih.gov/books/NBK56068/table/summarytables.t2/?report=objectonly',
    ACCEPTABLE_MACRONUTRIENT_DISTRIBUTION_RANGES := 'https://www.ncbi.nlm.nih.gov/books/NBK56068/table/summarytables.t5/?report=objectonly',
]

import glob, os
table_files = glob.glob("./dietary-requirements/*.txt")

for file in table_files:
    
    with open(file, 'r') as f:
        html_code = f.read().replace('\n', '')

    df = pd.read_html(str(html_code))[0]

    file = file[:-4]

    df.to_csv(f'./{file}.csv')