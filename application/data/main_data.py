
import pandas as pd

powerball = pd.read_csv('application/data/powerball.csv')

# Convert the date column to datetime format
powerball['Draw Date'] = pd.to_datetime(powerball['Draw Date'], format='%m/%d/%Y')

# Sort the DataFrame by the date column
powerball_sorted = powerball.sort_values(by='Draw Date')

# Optionally, if you want to reset the index after sorting
powerball_sorted.reset_index(drop=True, inplace=True)

# Filter rows based on the condition (in this case Date)
powerball_filtered= powerball_sorted[powerball_sorted['Draw Date'] >= '2015-10-04']

# Split the string by spaces and convert each part to integers
powerball_filtered['Winning Numbers'] = powerball_filtered['Winning Numbers'].apply(lambda x: [int(num) for num in x.split()])

# Extract the last number from each list and assign it to a new column
powerball_filtered['Red Ball'] = powerball_filtered['Winning Numbers'].apply(lambda x: x.pop())

# Reset index 
powerball_filtered.reset_index(drop=True, inplace=True)

# Rearrange columns
powerball_filtered = powerball_filtered[['Draw Date', 'Winning Numbers', 'Red Ball', 'Multiplier']]

# Convert Multiplier numbers from floats to integers
powerball_filtered['Multiplier'] = powerball_filtered['Multiplier'].astype(int)

# Explode the lists into separate rows to isolate individual White Numbers
powerball_exploded = powerball_filtered.explode('Winning Numbers')

# Find the last draw date
last_draw = powerball_filtered['Draw Date'].max()
# get date only from pandas date object to export to html
latest = last_draw.date()

# Subtract 6 months from the maximum date
six_months_ago = last_draw - pd.DateOffset(months=6)

#Ranged data for the last six months
start_date = last_draw 
end_date = six_months_ago

# get dataframe for the last six months
powerball_6_months = powerball_filtered[(powerball_filtered['Draw Date'] <= start_date) & (powerball_filtered['Draw Date'] >= end_date)]

# Explode Winning Numbers column to get each number separately
powerball_explode_6 = powerball_6_months.explode('Winning Numbers')
