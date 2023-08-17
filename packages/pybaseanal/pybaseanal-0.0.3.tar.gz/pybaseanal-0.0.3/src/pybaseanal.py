import pandas as pd, numpy as np, seaborn as sns, matplotlib.pyplot as plt

import warnings
warnings.filterwarnings('ignore')

def null_Analysis(data_df, null_Cuttoff = 25, headcount = 5):
    print('Total Data Size {0} and total number of columns are {1}'.format((len(data_df)),(len(data_df.columns))))
    null_df = pd.DataFrame(columns=['Feature', 'Total  Non-Null Value', 'No. of Null Value', '% NUll Value', 'Data Type'])
    feature = []
    total_val = []
    null_val = []
    per_null_val = []
    data_type = []
    for i in data_df.columns:
        feature.append(i)
        total_val.append(data_df[i].count())
        null_val.append(data_df[i].isnull().sum())
        per_null_val.append((data_df[i].isnull().sum() / len(data_df))*100)
        data_type.append(data_df[i].dtypes)
    null_df['Feature'] = feature
    null_df['Total  Non-Null Value'] = total_val
    null_df['No. of Null Value'] = null_val
    null_df['% NUll Value'] = per_null_val
    null_df['Data Type'] = data_type
    null_df =  null_df.sort_values(by='% NUll Value', axis=0, ascending=False)
    null_df = null_df.reset_index()
    null_df.drop('index', axis=1, inplace=True)
    high_null_column = []
    low_null_val = []
    for i,j in zip (null_df['Feature'], null_df['% NUll Value']):
        if j > null_Cuttoff:
            high_null_column.append(i)
        elif j < null_Cuttoff and j > 0:
            low_null_val.append(i)
    print('Columns with more than {0}% of null value : {1}'.format(null_Cuttoff, high_null_column) )
    print("")
    print('Columns with less than {0}% of null value : {1}'.format(null_Cuttoff, low_null_val) )
    print("")
    print("*************************")
    print("*** Dataframe Summary ***")
    print("*************************")
    for i in range (0, len(null_df)):
        print("Feature : {0} || Data Type : {1} ". format( null_df['Feature'].iloc[i], null_df['Data Type'].iloc[i]))
        print("No. of Null Value : {0} || Total Non-Null Value : {1} || % NUll Value : {2}".format(null_df['No. of Null Value'].iloc[i],null_df['Total  Non-Null Value'].iloc[i],null_df['% NUll Value'].iloc[i]))
        print('===========')
