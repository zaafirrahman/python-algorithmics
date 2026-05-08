import pandas as pd
df = pd.read_csv('GooglePlayStore_wild.csv')


# Cleaning data from the first task
df['Rating'].fillna(-1, inplace = True)


def set_size(size):
  if size[-1] == 'M':
     return float(size[:-1])
  elif size[-1] == 'k':
     return float(size[:-1]) / 1024
  return -1
df['Size'] = df['Size'].apply(set_size)


def set_installs(installs):
  if installs == '0':
      return 0
  return int(installs[:-1].replace(',', ''))
df['Installs'] = df['Installs'].apply(set_installs)


df['Type'].fillna('Free', inplace = True)


# Replace the data type with a fractional number (float) for the app prices ('Price')
def make_price(price):
 if price[0] == '$':
     return float(price[1:])
 return 0
df['Price'] = df['Price'].apply(make_price)


# Calculate how many dollars the developers earned on each paid app
df['Profit'] = df['Installs'] * df['Price']


# What is the maximum profit ('Profit') among the paid apps (Type == 'Paid')?
print(df[df['Type'] == 'Paid']['Profit'].max())


# Create a new column that will store the number of genres. Call it 'Number of genres'
def split_genres(genres):
   return genres.split(';')


df['Genres'] = df['Genres'].apply(split_genres)
df['Number of genres'] = df['Genres'].apply(len)


# What is the maximum 'Number of genres' stored in the dataset?
print(df['Number of genres'].max())


# Bonus task
# Create a new column storing the season in which the app was 'Last Updated'. Call it 'Season'
def set_season(date):
   month = date.split()[0]
   seasons = {'Winter': ['December', 'January', 'February'],
              'Spring': ['March', 'April', 'May'],
              'Summer': ['June', 'July', 'August'],
              'Autumn': ['September', 'October', 'November']}
   for season in seasons:
       if month in seasons[season]:
           return season
   return 'Season not identified'


df['Season'] = df['Last Updated'].apply(set_season)


# Display the seasons and how many there are in the dataset
print(df['Season'].value_counts())
