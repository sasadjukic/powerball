
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

