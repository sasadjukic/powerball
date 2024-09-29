
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
latest = last_draw.date()

# get date only from pandas date object to export to html
earliest = first_draw.date()

def next_draw():
    event_days = [0, 2, 5]
    today = datetime.date.today()
    
    for i in range(7):
        next_date = today + datetime.timedelta(days=i)
        if next_date.weekday() in event_days:
            return next_date