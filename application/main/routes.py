

from flask import render_template, Blueprint, request
from application.data.main_data import latest, earliest, next_draw
from application.data.user_search import (generate_percentage, white_balls, red_balls,
                                          get_streak, get_drought,
                                          get_red_drought, get_red_streak,
                                          monthly_number, monthly_number_red,
                                          yearly_number, yearly_number_red)
from application.data.matrix_data import m_data
from application.data.user_search_monthly import per_month, white_monthly_winners
from application.data.user_search_monthly_red import red_monthly_winners
from application.data.user_search_yearly import per_year, white_yearly_winners
from application.data.user_search_yearly_red import red_yearly_winners
from application.data.recent_winners import get_recent
from application.data.all_time_winners_white import all_time_white_winners
from application.data.all_time_winners_red import all_time_red_winners
from application.data.recent_winners_white import recent_white_winners
from application.data.recent_winners_red import recent_red_winners

powerball = Blueprint('powerball', __name__)

@powerball.route('/')
def home():
    return render_template('index.html', latest=latest)

@powerball.route('/rules', methods=['POST', 'GET'])
def rules():
    return render_template('rules.html')

@powerball.route('/all_time_winners', methods=['POST', 'GET'])
def all_time_winners():
    # Generate bar charts for all time winners
    white_all_time = all_time_white_winners()
    red_all_time = all_time_red_winners()
    return render_template('winners.html', 
                            white_all_time=white_all_time, 
                            red_all_time=red_all_time
                            )

@powerball.route('/top_6_months', methods=['POST', 'GET'])
def top_6_months():
    # Generate bar charts for top 6 months
    white_top_6 = recent_white_winners()
    red_top_6 = recent_red_winners()
    return render_template('winners_6m.html', 
                            white_top_6=white_top_6, 
                            red_top_6=red_top_6
                            )

@powerball.route('/recent_winners', methods=['POST', 'GET'])
def recent_winners():
    # Get recent powerball winners with draw dates
    recent = get_recent()
    return render_template('recent_winners.html', 
                            recent = recent
                            )

@powerball.route('/search', methods=['POST', 'GET'])
def search():
    number = None
    if request.method == 'POST':
        # Get user input for a powerball number they want to search
        number = int(request.form['number_input'])

        # if user number is less than 70, then fetch white balls
        if number < 70:
            # Get number of times searched number appears
            white_occurrences = white_balls(number)
            # Generate percentage
            white_percentage = generate_percentage(white_occurrences)

            white_droughts = get_drought(number)
            white_streaks = get_streak(number)

            monthly_winners = monthly_number(number)
            months = {1:0, 2:0, 3:0, 4:0, 5:0, 6:0, 7:0, 8:0, 9:0, 10:0, 11:0, 12:0}
            pm = per_month(monthly_winners, months)
            chart_white_monthly = white_monthly_winners(number, pm)

            yearly_winners = yearly_number(number)
            py = per_year(yearly_winners)
            chart_white_yearly = white_yearly_winners(number, py)

            # if user number is less than 26, then fetch both white and red balls 
            if number <= 26:
                red_occurrences = red_balls(number)
                red_percentage = generate_percentage(red_occurrences)
                red_drought = get_red_drought(number)
                red_streak = get_red_streak(number)

                monthly_winner_red = monthly_number_red(number)
                months_red = {1:0, 2:0, 3:0, 4:0, 5:0, 6:0, 7:0, 8:0, 9:0, 10:0, 11:0, 12:0}
                pm_red = per_month(monthly_winner_red, months_red)
                chart_red_monthly = red_monthly_winners(number, pm_red)

                yearly_winner_red = yearly_number_red(number)
                py_red = per_year(yearly_winner_red)
                chart_red_yearly = red_yearly_winners(number, py_red)
                
                return render_template('search.html', number=number, 
                                        red_occurrences=red_occurrences, 
                                        red_percentage=red_percentage, 
                                        red_drought=red_drought,
                                        red_streak=red_streak,
                                        white_occurrences=white_occurrences, 
                                        white_percentage=white_percentage, 
                                        white_droughts=white_droughts,
                                        white_streaks=white_streaks,
                                        earliest=earliest,
                                        latest=latest,
                                        chart_white_monthly = chart_white_monthly,
                                        chart_red_monthly = chart_red_monthly,
                                        chart_white_yearly = chart_white_yearly,
                                        chart_red_yearly = chart_red_yearly
                                        )

            return render_template('search.html', number=number, 
                                    white_occurrences=white_occurrences, 
                                    white_percentage=white_percentage, 
                                    earliest=earliest,
                                    latest=latest,
                                    white_droughts=white_droughts,
                                    white_streaks=white_streaks,
                                    chart_white_monthly = chart_white_monthly,
                                    chart_white_yearly = chart_white_yearly
                                    )
    
    return render_template('search.html', number=number)


@powerball.route('/winning_hands_white', methods=['POST', 'GET'])
def winning_hands_white():
    splits = {
              'all-time': [3367, 3438, 6895],
              'six-months': [182, 213, 400],
              'recent-trends': [61, 68, 130]
            }

    sets = {
            'all-time' : [875, 963, 1019, 1024, 956, 995, 1063, 6895],
            'six-months' : [49, 59, 50, 54, 62, 70, 56, 400],
            'recent-trends' : [18, 23, 14, 15, 21, 25, 14, 130]
    }

    winning_hands = {
                     'singles': [231, 15, 6], 'pairs': [715, 42, 11], 
                     'two_pairs': [257, 15, 7], 'three_of_set': [144, 6, 2], 
                     'full_house': [21, 1, 0], 'poker': [11, 1, 0], 'flush': [0, 0, 0]
                     }
    total_winning_hands = sum(values[0] for values in winning_hands.values())
    total_winning_hands_6 = sum(values[1] for values in winning_hands.values())
    total_winning_hands_recent = sum(values[2] for values in winning_hands.values())

    pair_count = {
                  1: [83, 4, 2], 10: [93, 7, 2], 20: [120, 4, 0], 30: [107, 2, 0], 
                  40: [91, 10, 3], 50: [105, 7, 3], 60: [115, 8, 1]
                }
    total_pairs = sum(values[0] for values in pair_count.values())
    total_pairs_6 = sum(values[1] for values in pair_count.values())
    total_pairs_recent = sum(values[2] for values in pair_count.values())

    return render_template('winning_hands.html',
                           splits=splits,
                           sets=sets,
                           winning_hands=winning_hands,
                           total_winning_hands=total_winning_hands,
                           total_winning_hands_6=total_winning_hands_6,
                           total_winning_hands_recent=total_winning_hands_recent, 
                           pair_count=pair_count, 
                           total_pairs=total_pairs,
                           total_pairs_6=total_pairs_6,
                           total_pairs_recent=total_pairs_recent
                           )

@powerball.route('/winning_hands_red', methods=['POST', 'GET'])
def winning_hands_red():
    splits = {
              'all-time': [683, 696, 1379],
              'six-months': [45, 35, 80], 
              'recent-trends': [17, 9, 26]
            }

    sets = {
            'all-time' : [489, 498, 392, 1379],
            'six-months' : [30, 29, 21, 80],
            'recent-trends' : [10, 13, 3, 26]
           }

    return render_template('winning_hands_red.html', 
                           splits=splits,
                           sets=sets
                           )

@powerball.route('/trends', methods=['POST', 'GET'])
def trends():
    white_numbers_6 = [
                       1, 7, 9, 5, 5, 7, 6, 4, 5, 5, 
                       5, 4, 5, 9, 1, 9, 8, 8, 5, 4, 
                       8, 4, 3, 5, 5, 3, 6, 7, 5, 8, 
                       7, 3, 3, 3, 5, 9, 7, 7, 2, 5, 
                       6, 9, 6, 7, 3, 5, 8, 8, 5, 8, 
                       5, 10, 6, 3, 8, 9, 6, 7, 8, 8, 
                       5, 3, 9, 11, 7, 4, 3, 4, 2
                    ]

    white_numbers_trends = [
                        1, 4, 4, 1, 3, 1, 1, 1, 2, 2, 
                        0, 2, 2, 6, 0, 5, 4, 1, 1, 1, 
                        3, 1, 0, 1, 2, 2, 1, 1, 2, 1, 
                        2, 2, 0, 1, 1, 1, 1, 5, 1, 1, 
                        1, 1, 2, 6, 2, 1, 1, 4, 2, 5, 
                        1, 1, 4, 0, 4, 1, 2, 2, 5, 3, 
                        1, 1, 1, 3, 0, 2, 1, 1, 1
                    ]

    red_numbers_6 = [
                     6, 3, 6, 2, 5, 6, 1, 1, 0, 2, 
                     3, 6, 4, 4, 5, 1, 1, 3, 0, 5, 
                     2, 1, 3, 4, 2, 4
                    ]

    red_numbers_trends = [
                          1, 1, 4, 1, 1, 1, 0, 1, 0, 1, 
                          1, 3, 2, 3, 1, 1, 0, 1, 0, 2, 
                          0, 0, 1, 0, 0, 0
                         ]
                         
    return render_template('trends.html',
                            white_numbers_6 = white_numbers_6,
                            white_numbers_trends = white_numbers_trends,
                            red_numbers_6 = red_numbers_6,
                            red_numbers_trends = red_numbers_trends
                          )

@powerball.route('/powerball_matrix', methods=['POST', 'GET'])
def powerball_matrix():
    number = None
    if request.method == 'POST':
        # Get user input for a powerball number they want to search
        number = int(request.form['matrix-input'])

    return render_template('powerball_matrix.html', 
                            number=number, 
                            m_data=m_data
                            )

@powerball.route('/fun_facts', methods=['POST', 'GET'])
def fun_facts():
    return render_template('fun_facts.html')

@powerball.route('/probabilities', methods=['POST', 'GET'])
def probabilities():
    draw = next_draw().strftime('%m-%d-%Y')
    white_numbers = [
                     6.74, 7.29, 7.94, 6.89, 6.58, 7.42, 6.97, 6.45, 6.44, 6.97, 
                     7.16, 7.70, 5.69, 6.11, 6.70, 8.09, 6.87, 7.40, 7.21, 7.07, 
                     8.29, 6.93, 8.78, 7.74, 6.49, 6.26, 8.37, 8.80, 7.09, 6.95, 
                     7.32, 7.85, 8.33, 6.32, 6.22, 8.60, 8.28, 6.84, 7.74, 7.18, 
                     6.16, 7.01, 7.35, 8.13, 7.03, 5.94, 7.49, 6.39, 5.72, 7.14, 
                     6.32, 7.49, 8.21, 7.01, 6.70, 6.82, 6.83, 7.00, 7.62, 6.89, 
                     8.98, 7.99, 8.31, 8.42, 6.44, 7.49, 7.27, 7.24, 8.54
                     ]
    red_numbers = [
                   4.05, 3.39, 4.19, 4.96, 4.11, 3.56, 3.14, 3.11, 4.17, 3.50, 
                   3.62, 3.36, 3.46, 4.88, 3.23, 3.16, 3.42, 4.46, 3.81, 4.36, 
                   4.46, 3.54, 3.42, 4.50, 4.03, 4.11
                   ]
    return render_template('probabilities.html', 
                            draw=draw,
                            white_numbers=white_numbers, 
                            red_numbers=red_numbers
                        )

@powerball.route('/predictions', methods=['POST', 'GET'])
def predictions():
    draw = next_draw().strftime('%m-%d-%Y')
    white_numbers = [
                     [1, 9, 35, 38, 42],
                     [3, 12, 32, 45, 68],
                     [1, 14, 43, 52, 57],
                     [6, 8, 26, 34, 54],
                     [7, 15, 34, 67, 69]
                     ]
    red_numbers = [1, 14, 19, 20, 21]
    return render_template('predictions.html',
                            draw=draw, 
                            white_numbers=white_numbers, 
                            red_numbers=red_numbers
                            )