
from application.data.main_data import powerball, powerball_exploded
import pandas as pd

def white_balls(n: int) -> int:
    #powerball_explode = powerball_user.explode('Winning Numbers')
    return (powerball_exploded['Winning Numbers'] == n).sum()

def red_balls(n: int) -> int:
    return (powerball['Red Ball'] == n).sum()

def generate_percentage(user_input: int) -> float:
    return round((user_input / powerball.shape[0]) * 100, 2)

# find maximum and current DROUGHTS where a user input number HAS NOT been drawn
# this refers to actual powerball draws, and draws are held every Monday, Wednesday and Saturday
def get_drought(n: int) -> list[int]:
    
    current_drought = 0
    max_drought = 0
    for bucket in powerball['Winning Numbers']:
        if n not in bucket:
            current_drought += 1
            if max_drought < current_drought:
                max_drought = current_drought
        else:
            if max_drought < current_drought:
                max_drought = current_drought
            current_drought = 0

    return [max_drought, current_drought]

# find a STREAK (if there is any) where a user input number HAS BEEN drawn
# a streak (in this case) refers to consecutive months the ball has been drawn, not consecutive draws
def get_streak(n: int) -> list[int]:
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

def get_red_drought(n: int) -> list[int]:
    
    current_drought = 0
    max_drought = 0
    for number in powerball['Red Ball']:
        if n != number:
            current_drought += 1
            if max_drought < current_drought:
                max_drought = current_drought
        else:
            if max_drought < current_drought:
                max_drought = current_drought
            current_drought = 0

    return [max_drought, current_drought]

def get_red_streak(n: int) -> list[int]:
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

# find at what dates a user number was drawn as white ball winner
def monthly_number(n: int):
    number = powerball_exploded[powerball_exploded['Winning Numbers'] == n]
    all_winners = number['Draw Date'].dt.month.tolist()
    return all_winners

def monthly_number_red(n:int):
    r_number = powerball[powerball['Red Ball'] == n]
    all_winners = r_number['Draw Date'].dt.month.tolist()
    return all_winners

def yearly_number(n: int):
    number = powerball_exploded[powerball_exploded['Winning Numbers'] == n]
    all_winners = number['Draw Date'].dt.year.tolist()
    return all_winners

def yearly_number_red(n:int):
    r_number = powerball[powerball['Red Ball'] == n]
    all_winners = r_number['Draw Date'].dt.year.tolist()
    return all_winners

