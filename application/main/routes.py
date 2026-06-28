

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
              'all-time': [3342, 3408, 6840],
              'six-months': [188, 207, 400],
              'recent-trends': [56, 72, 130]
            }

    sets = {
            'all-time' : [864, 954, 1014, 1019, 947, 984, 1058, 6840],
            'six-months' : [46, 58, 57, 55, 58, 71, 55, 400],
            'recent-trends' : [11, 20, 14, 20, 22, 22, 21, 130]
    }

    winning_hands = {
                     'singles': [229, 15, 7], 'pairs': [710, 45, 12], 
                     'two_pairs': [254, 13, 5], 'three_of_set': [143, 5, 2], 
                     'full_house': [21, 1, 0], 'poker': [11, 1, 0], 'flush': [0, 0, 0]
                     }
    total_winning_hands = sum(values[0] for values in winning_hands.values())
    total_winning_hands_6 = sum(values[1] for values in winning_hands.values())
    total_winning_hands_recent = sum(values[2] for values in winning_hands.values())

    pair_count = {
                  1: [81, 3, 0], 10: [92, 7, 1], 20: [120, 5, 0], 30: [107, 3, 1], 
                  40: [90, 9, 4], 50: [104, 10, 3], 60: [115, 8, 3]
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
              'all-time': [675, 693, 1368],
              'six-months': [40, 40, 80], 
              'recent-trends': [13, 13, 26]
            }

    sets = {
            'all-time' : [481, 496, 391, 1368],
            'six-months' : [25, 31, 24, 80],
            'recent-trends' : [4, 17, 5, 26]
           }

    return render_template('winning_hands_red.html', 
                           splits=splits,
                           sets=sets
                           )

@powerball.route('/trends', methods=['POST', 'GET'])
def trends():
    white_numbers_6 = [
                       1, 4, 9, 6, 7, 7, 5, 4, 3, 3, 
                       7, 3, 5, 6, 2, 9, 6, 10, 7, 5, 
                       11, 3, 3, 8, 5, 2, 8, 9, 3, 8, 
                       8, 3, 3, 5, 5, 8, 6, 6, 3, 5, 
                       5, 9, 6, 4, 3, 4, 8, 8, 6, 5, 
                       7, 11, 6, 3, 7, 10, 8, 7, 7, 9, 
                       5, 4, 9, 12, 7, 3, 2, 3, 1
                    ]

    white_numbers_trends = [
                        1, 1, 5, 2, 1, 0, 0, 1, 0, 1, 
                        0, 1, 3, 3, 1, 6, 2, 1, 2, 1, 
                        3, 1, 0, 2, 2, 1, 2, 2, 0, 4, 
                        3, 2, 0, 2, 2, 1, 3, 3, 0, 1, 
                        2, 3, 1, 4, 1, 2, 2, 4, 2, 2, 
                        3, 3, 2, 0, 3, 3, 3, 1, 2, 4, 
                        2, 1, 1, 4, 4, 2, 2, 1, 0
                    ]

    red_numbers_6 = [
                     6, 4, 3, 2, 4, 5, 1, 0, 0, 2, 
                     3, 6, 4, 7, 5, 0, 1, 2, 1, 4, 
                     3, 1, 5, 4, 2, 5
                    ]

    red_numbers_trends = [
                          0, 1, 1, 0, 1, 0, 1, 0, 0, 1, 
                          1, 4, 3, 4, 3, 0, 0, 1, 0, 1, 
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
                     6.44, 6.93, 8.21, 6.63, 6.02, 7.31, 7.31, 6.76, 6.46, 6.79, 
                     7.47, 7.60, 6.21, 6.52, 6.74, 7.57, 7.44, 7.36, 7.27, 7.02, 
                     9.18, 6.88, 8.88, 7.17, 6.33, 5.69, 8.59, 8.41, 6.17, 7.16, 
                     7.38, 8.28, 8.60, 5.56, 6.43, 8.21, 7.58, 6.83, 7.49, 7.44, 
                     6.79, 6.61, 7.34, 8.40, 7.61, 6.24, 7.57, 6.18, 6.22, 7.19, 
                     6.89, 7.51, 7.84, 6.63, 6.27, 6.94, 7.12, 6.40, 7.85, 6.73, 
                     9.35, 8.18, 8.48, 9.35, 6.40, 7.29, 7.42, 6.84, 8.04
                     ]
    red_numbers = [
                   4.28, 3.61, 4.19, 4.87, 4.21, 3.51, 3.34, 3.11, 3.81, 2.95, 
                   3.74, 3.53, 3.58, 4.83, 3.73, 3.03, 3.38, 3.95, 4.01, 4.62, 
                   4.72, 3.16, 3.17, 4.35, 4.35, 3.97
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
                     [2, 42, 46, 47, 69],
                     [30, 36, 39, 43, 61],
                     [9, 28, 32, 54, 62],
                     [15, 27, 28, 35, 53],
                     [5, 6, 12, 56, 65]
                     ]
    red_numbers = [3, 4, 6, 21, 25]
    return render_template('predictions.html',
                            draw=draw, 
                            white_numbers=white_numbers, 
                            red_numbers=red_numbers
                            )