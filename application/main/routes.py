

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
              'all-time': [3152, 3198, 6435],
              'six-months': [202, 191, 400],
              'recent-trends': [65, 64, 130]
            }

    sets = {
            'all-time' : [817, 895, 957, 963, 888, 912, 1003, 6435],
            'six-months' : [55, 57, 58, 51, 52, 54, 73, 400],
            'recent-trends' : [19, 16, 19, 17, 14, 23, 22, 130]
    }

    winning_hands = {
                     'singles': [213, 18, 7], 'pairs': [665, 41, 16], 
                     'two_pairs': [241, 13, 2], 'three_of_set': [138, 6, 1], 
                     'full_house': [20, 2, 0], 'poker': [10, 0, 0], 'flush': [0, 0, 0]
                     }
    total_winning_hands = sum(values[0] for values in winning_hands.values())
    total_winning_hands_6 = sum(values[1] for values in winning_hands.values())
    total_winning_hands_recent = sum(values[2] for values in winning_hands.values())

    pair_count = {
                  1: [78, 2, 2], 10: [85, 4, 1], 20: [115, 5, 0], 30: [104, 3, 2], 
                  40: [81, 10, 3], 50: [94, 8, 4], 60: [107, 8, 4]
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
              'all-time': [634, 653, 1287],
              'six-months': [34, 46, 80], 
              'recent-trends': [9, 17, 26]
            }

    sets = {
            'all-time' : [455, 465, 367, 1287],
            'six-months' : [27, 26, 27, 80],
            'recent-trends' : [7, 8, 11, 26]
           }

    return render_template('winning_hands_red.html', 
                           splits=splits,
                           sets=sets
                           )

@powerball.route('/trends', methods=['POST', 'GET'])
def trends():
    white_numbers_6 = [
                       4, 5, 9, 6, 4, 4, 8, 11, 4, 5, 
                       5, 5, 5, 6, 7, 9, 3, 6, 6, 2, 
                       2, 5, 6, 4, 5, 5, 5, 16, 8, 3, 
                       6, 10, 8, 5, 7, 3, 4, 2, 3, 6, 
                       2, 5, 8, 8, 4, 4, 5, 4, 6, 7, 
                       8, 7, 9, 5, 2, 1, 4, 6, 5, 5, 
                       9, 10, 4, 9, 7, 8, 7, 5, 9
                    ]

    white_numbers_trends = [
                        2, 2, 2, 2, 2, 2, 3, 3, 1, 2, 
                        0, 2, 1, 2, 1, 2, 2, 2, 2, 1, 
                        0, 2, 1, 1, 1, 4, 0, 6, 3, 2, 
                        2, 4, 3, 0, 1, 1, 1, 0, 3, 1, 
                        0, 0, 4, 3, 0, 1, 2, 1, 2, 1, 
                        5, 3, 3, 1, 0, 1, 3, 3, 3, 3, 
                        1, 3, 1, 1, 2, 4, 1, 3, 3
                    ]

    red_numbers_6 = [
                     5, 6, 3, 3, 4, 1, 1, 2, 2, 2, 
                     2, 3, 0, 4, 3, 2, 3, 3, 4, 5, 
                     3, 6, 6, 2, 3, 2
                    ]

    red_numbers_trends = [
                          3, 2, 1, 0, 0, 0, 1, 0, 0, 0, 
                          1, 1, 0, 1, 1, 1, 1, 1, 1, 2, 
                          1, 2, 4, 0, 0, 2
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
                     6.90, 7.20, 7.66, 6.92, 6.81, 7.21, 6.76, 7.23, 7.04, 6.77, 
                     6.79, 8.15, 5.54, 6.64, 7.31, 7.91, 6.82, 7.23, 7.10, 7.37, 
                     8.79, 6.97, 8.73, 7.59, 6.26, 5.89, 8.52, 8.17, 7.05, 6.70, 
                     6.92, 8.68, 8.83, 5.94, 6.64, 7.99, 7.89, 6.76, 8.30, 7.51, 
                     6.52, 6.51, 6.79, 7.49, 7.54, 6.18, 7.48, 6.30, 5.87, 6.96, 
                     6.59, 7.52, 8.23, 6.89, 6.43, 6.84, 6.77, 6.73, 7.86, 6.44, 
                     8.89, 8.19, 8.10, 8.54, 6.05, 7.68, 7.74, 7.13, 8.25
                     ]
    red_numbers = [
                   4.12, 3.45, 3.84, 4.80, 4.48, 3.62, 3.27, 3.04, 4.57, 3.45, 
                   3.71, 3.01, 3.62, 4.51, 3.14, 3.26, 3.17, 4.38, 3.93, 4.23, 
                   4.39, 3.78, 3.47, 4.53, 4.42, 3.81
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
                     [3, 19, 21, 32, 64],
                     [5, 15, 33, 63, 67],
                     [6, 7, 34, 53, 69],
                     [2, 9, 28, 38, 46],
                     [10, 14, 22, 23, 29]
                     ]
    red_numbers = [1, 8, 11, 17, 19]
    return render_template('predictions.html',
                            draw=draw, 
                            white_numbers=white_numbers, 
                            red_numbers=red_numbers
                            )