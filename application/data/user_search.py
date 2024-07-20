
from application.data.main_data import powerball_filtered
import pandas as pd

def white_balls(n: int, powerball_user: pd.DataFrame) -> int:
    powerball_explode = powerball_user.explode('Winning Numbers')
    return (powerball_explode['Winning Numbers'] == n).sum()

def red_balls(n: int, powerball_user: pd.DataFrame) -> int:
    return (powerball_user['Red Ball'] == n).sum()

def generate_percentage(user_input: int, total_draws: int) -> float:
    return round((user_input / total_draws) * 100, 2)

# create a function to generate new dataframe based on a date input from user
def date_search(date_input: str, start_date: str) -> pd.DataFrame:
    return powerball_filtered[(powerball_filtered['Draw Date'] >= date_input) & (powerball_filtered['Draw Date'] <= start_date)]

# find maximum and current DRAUGHTS where a user input number HAS NOT been drawn
# this refers to actual powerball draws, and draws are held every Monday, Wednesday and Saturday
def get_draught(n: int, powerball: pd.DataFrame) -> list[int]:
    
    current_draught = 0
    max_draught = 0
    for bucket in powerball['Winning Numbers']:
        if n not in bucket:
            current_draught += 1
        else:
            if max_draught < current_draught:
                max_draught = current_draught
            current_draught = 0

    return [max_draught, current_draught]

# find a STREAK (if there is any) where a user input number HAS BEEN drawn
# a streak (in this case) refers to consecutive months the ball has been drawn, not consecutive draws
def get_streak(n: int, powerball: pd.DataFrame) -> list[int]:
    streak = 0
    max_streak = 0
    winning_month = 0
    winnining_year = powerball['Draw Date'].iloc[0].year
    for i in powerball.index:
        month = powerball.loc[i, 'Draw Date'].month
        year = powerball.loc[i, 'Draw Date'].year

        if year != winnining_year:
            if abs(month - winning_month) != 11:
                streak = 0
                winning_month = 0

        if month - winning_month > 1:
            streak = 0

        if n in powerball.loc[i, 'Winning Numbers']:
            if month > winning_month:
                streak += 1
                winning_month = month
                winnining_year = year
                if streak > max_streak:
                    max_streak = streak

    # returns max streak and current streak
    return [max_streak, streak]

def get_red_draught(n: int, powerball: pd.DataFrame) -> list[int]:
    
    current_draught = 0
    max_draught = 0
    for number in powerball['Red Ball']:
        if n != number:
            current_draught += 1
        else:
            if max_draught < current_draught:
                max_draught = current_draught
            current_draught = 0

    return [max_draught, current_draught]

def get_red_streak(n: int, powerball: pd.DataFrame) -> list[int]:
    streak = 0
    max_streak = 0
    winning_month = 0
    winnining_year = powerball['Draw Date'].iloc[0].year
    for i in powerball.index:
        month = powerball.loc[i, 'Draw Date'].month
        year = powerball.loc[i, 'Draw Date'].year

        if year != winnining_year:
            if abs(month - winning_month) != 11:
                streak = 0
                winning_month = 0

        if month - winning_month > 1:
            streak = 0

        if n == powerball.loc[i, 'Red Ball']:
            if month > winning_month:
                streak += 1
                winning_month = month
                winnining_year = year
                if streak > max_streak:
                    max_streak = streak

    return [max_streak, streak]