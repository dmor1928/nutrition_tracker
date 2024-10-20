import pandas as pd

complete_nutritional_data = pd.read_csv('./clean-tables/complete_nutritional_data.csv')

columns = complete_nutritional_data.columns

returnValue = "'''<Foods("

for columnNum, column in enumerate(columns):
    returnValue += f"{column}=" + "'{" + f'{columnNum}' + "}', "

returnValue = returnValue[:-2]
returnValue += ")>'''"
returnValue += ".format("

for column in columns:
    returnValue += "self." + f'{column}' + ", "

returnValue = returnValue[:-2]
returnValue += ")"

print(returnValue)