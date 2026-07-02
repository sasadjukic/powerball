

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
              'all-time': [3347, 3413, 6850],
              'six-months': [187, 208, 400],
              'recent-trends': [58, 71, 130]
            }

    sets = {
            'all-time' : [866, 956, 1015, 1020, 948, 986, 1059, 6850],
            'six-months' : [46, 60, 56, 53, 59, 71, 55, 400],
            'recent-trends' : [12, 21, 14, 19, 22, 22, 20, 130]
    }

    winning_hands = {
                     'singles': [229, 15, 5], 'pairs': [711, 44, 13], 
                     'two_pairs': [255, 14, 6], 'three_of_set': [143, 5, 2], 
                     'full_house': [21, 1, 0], 'poker': [11, 1, 0], 'flush': [0, 0, 0]
                     }
    total_winning_hands = sum(values[0] for values in winning_hands.values())
    total_winning_hands_6 = sum(values[1] for values in winning_hands.values())
    total_winning_hands_recent = sum(values[2] for values in winning_hands.values())

    pair_count = {
                  1: [82, 4, 1], 10: [92, 7, 1], 20: [120, 5, 0], 30: [107, 2, 1], 
                  40: [90, 9, 4], 50: [104, 9, 3], 60: [115, 8, 3]
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
              'all-time': [677, 693, 1370],
              'six-months': [41, 39, 80], 
              'recent-trends': [15, 11, 26]
            }

    sets = {
            'all-time' : [483, 496, 391, 1370],
            'six-months' : [26, 30, 24, 80],
            'recent-trends' : [6, 15, 5, 26]
           }

    return render_template('winning_hands_red.html', 
                           splits=splits,
                           sets=sets
                           )

@powerball.route('/trends', methods=['POST', 'GET'])
def trends():
    white_numbers_6 = [
                       1, 5, 9, 5, 6, 8, 5, 4, 3, 4, 
                       7, 3, 5, 7, 2, 9, 6, 10, 7, 4, 
                       11, 3, 3, 8, 4, 3, 8, 9, 3, 8, 
                       7, 3, 3, 4, 5, 8, 6, 6, 3, 5, 
                       6, 9, 6, 4, 3, 4, 8, 8, 6, 5, 
                       7, 10, 7, 3, 7, 10, 8, 7, 7, 9, 
                       5, 3, 9, 12, 7, 3, 2, 4, 1
                    ]

    white_numbers_trends = [
                        1, 2, 4, 2, 1, 1, 0, 1, 0, 2, 
                        0, 1, 3, 4, 1, 6, 2, 1, 1, 1, 
                        3, 1, 0, 2, 1, 2, 2, 2, 0, 4, 
                        3, 2, 0, 2, 1, 1, 2, 3, 1, 1, 
                        3, 2, 1, 4, 1, 2, 2, 4, 2, 2, 
                        2, 2, 3, 0, 3, 3, 3, 1, 3, 4, 
                        2, 1, 1, 4, 3, 2, 1, 2, 0
                    ]

    red_numbers_6 = [
                     5, 4, 4, 2, 4, 6, 1, 0, 0, 2, 
                     3, 6, 4, 7, 5, 0, 1, 2, 0, 4, 
                     3, 1, 5, 4, 2, 5
                    ]

    red_numbers_trends = [
                          0, 1, 2, 0, 1, 1, 1, 0, 0, 1, 
                          1, 4, 3, 3, 2, 0, 0, 1, 0, 1, 
                          0, 1, 1, 0, 1, 1
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
                     6.90, 6.75, 7.41, 6.94, 6.56, 7.56, 6.71, 6.99, 6.43, 6.82, 
                     7.11, 7.38, 5.78, 6.36, 6.76, 7.83, 6.67, 7.39, 6.88, 7.38, 
                     9.05, 6.65, 8.13, 6.48, 6.48, 5.94, 8.85, 8.67, 6.58, 6.99, 
                     7.05, 8.02, 8.58, 6.00, 6.44, 8.62, 8.28, 6.62, 7.81, 7.42, 
                     6.19, 6.84, 7.21, 7.67, 7.59, 6.01, 7.92, 6.73, 6.03, 7.18, 
                     6.55, 8.12, 8.09, 6.82, 6.65, 6.93, 7.14, 6.79, 8.07, 6.85, 
                     9.15, 8.19, 8.57, 8.73, 6.58, 7.25, 7.54, 6.89, 8.42
                     ]
    red_numbers = [
                   4.26, 3.93, 3.91, 4.51, 4.43, 3.53, 3.28, 3.48, 3.87, 3.50, 
                   3.43, 3.37, 4.00, 4.38, 3.11, 3.01, 3.26, 4.42, 3.80, 4.25, 
                   4.53, 3.13, 3.71, 4.66, 4.37, 3.81
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
                     [23, 29, 39, 50, 61],
                     [2, 9, 56, 68, 69],
                     [3, 27, 52, 56, 64],
                     [10, 17, 23, 52, 61],
                     [14, 21, 31, 33, 60]
                     ]
    red_numbers = [9, 13, 15, 20, 21]
    return render_template('predictions.html',
                            draw=draw, 
                            white_numbers=white_numbers, 
                            red_numbers=red_numbers
                            )