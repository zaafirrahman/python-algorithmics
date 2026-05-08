import pandas as pd
df = pd.read_csv('GooglePlayStore_wild.csv')
# Display the app with index 10472. See what mistakes were made in the values.
print(df.iloc[10472])


# Correct the mistakes in the values
columns = list(df.columns)
index = 10472
for i in range(len(columns) -1, 1, -1):
   df[columns[i]][index] = df[columns[i - 1]][index]


# There are some null values ('NaN') among the app values. Replace those null values with 'Lifestyle'.
df['Category'][index] = 'LIFESTYLE'
df['Genres'][index] = 'Lifestyle'


# Display the app to make sure the cleaning was successful
print(df.iloc[10472])