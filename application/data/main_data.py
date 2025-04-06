
import datetime
import pandas as pd

powerball = pd.read_csv('application/data/powerball.csv')

# Convert the date column to datetime format
powerball['Draw Date'] = pd.to_datetime(powerball['Draw Date'], format='%m/%d/%Y')

# Split the string by spaces and convert each part to integers
powerball['Winning Numbers'] = powerball['Winning Numbers'].apply(lambda x: [int(num) for num in x.split()])

# Explode the lists into separate rows to isolate individual White Numbers
powerball_exploded = powerball.explode('Winning Numbers')

# Find the last draw date
last_draw = powerball['Draw Date'].max()

# Find the first draw date
first_draw = powerball['Draw Date'].min()

# get date only from pandas date object to export to html
latest = last_draw.date().strftime('%m-%d-%Y')

# Get date only from pandas date object to export to html
earliest = first_draw.date().strftime('%m-%d-%Y')

# Get dataframe for the last six months
powerball_6_months = powerball.tail(80)

# Explode Winning Numbers column to get each number separately
powerball_explode_6 = powerball_6_months.explode('Winning Numbers')

# Find next draw
def next_draw():
    l_draw = powerball['Draw Date'].max().date()
    
    if l_draw.weekday() == 2:
        return l_draw + datetime.timedelta(days=3)

    return l_draw + datetime.timedelta(days=2)