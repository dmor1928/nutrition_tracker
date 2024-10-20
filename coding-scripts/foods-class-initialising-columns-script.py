import pandas as pd

complete_nutritional_data = pd.read_csv('./clean-tables/complete_nutritional_data.csv')

columns = complete_nutritional_data.columns

for column in columns:

    if column == 'id':
        bracketExpression = 'Integer'
    elif column == 'name':
        bracketExpression = 'String(250), primary_key=True'
    else:
        bracketExpression = 'Float'
    print(f'{column} = Column({bracketExpression})')

