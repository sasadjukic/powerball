
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

# Get date only from pandas date object to export to html
earliest = first_draw.date()

# Subtract 6 months from the maximum date
six_months_ago = last_draw - pd.DateOffset(months=6)

# Ranged data for the last six months
start_date_6 = last_draw 
end_date_6 = six_months_ago

# Get dataframe for the last six months
powerball_6_months = powerball[(powerball['Draw Date'] <= start_date_6) & (powerball['Draw Date'] >= end_date_6)]

# Explode Winning Numbers column to get each number separately
powerball_explode_6 = powerball_6_months.explode('Winning Numbers')

# Find next draw
def next_draw():
    event_days = [0, 2, 5]
    today = datetime.date.today()
    
    for i in range(7):
        next_date = today + datetime.timedelta(days=i)
        if next_date.weekday() in event_days:
            return next_date