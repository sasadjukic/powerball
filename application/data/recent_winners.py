

from application.data.main_data import powerball

recent = powerball.tail(26)
reverse_r = recent.iloc[::-1]

#get last 12 draws with dates, winning white numbers and winning red numbers
def get_recent() -> tuple[list, list, list]:

    dates = []
    numbers = []
    powerballs = []

    for i in range(len(reverse_r)):
        date = reverse_r.iloc[i, 0].strftime("%m-%d-%Y")
        white_numbers = reverse_r.iloc[i, 1]
        powerball = reverse_r.iloc[i, 2]

        dates.append(date)
        numbers.append(white_numbers)
        powerballs.append(powerball)

    return dates, numbers, powerballs