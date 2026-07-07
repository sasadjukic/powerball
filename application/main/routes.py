

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
              'all-time': [3349, 3421, 6860],
              'six-months': [182, 213, 400],
              'recent-trends': [57, 72, 130]
            }

    sets = {
            'all-time' : [866, 958, 1015, 1021, 950, 987, 1063, 6860],
            'six-months' : [46, 58, 54, 52, 60, 71, 59, 400],
            'recent-trends' : [12, 22, 13, 18, 23, 22, 20, 130]
    }

    winning_hands = {
                     'singles': [230, 16, 6], 'pairs': [711, 43, 12], 
                     'two_pairs': [255, 13, 5], 'three_of_set': [144, 6, 3], 
                     'full_house': [21, 1, 0], 'poker': [11, 1, 0], 'flush': [0, 0, 0]
                     }
    total_winning_hands = sum(values[0] for values in winning_hands.values())
    total_winning_hands_6 = sum(values[1] for values in winning_hands.values())
    total_winning_hands_recent = sum(values[2] for values in winning_hands.values())

    pair_count = {
                  1: [82, 4, 1], 10: [92, 6, 1], 20: [120, 5, 0], 30: [107, 2, 1], 
                  40: [90, 9, 4], 50: [104, 9, 3], 60: [115, 8, 2]
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
              'all-time': [678, 694, 1372],
              'six-months': [42, 38, 80], 
              'recent-trends': [14, 12, 26]
            }

    sets = {
            'all-time' : [484, 496, 392, 1372],
            'six-months' : [27, 30, 23, 80],
            'recent-trends' : [6, 14, 6, 26]
           }

    return render_template('winning_hands_red.html', 
                           splits=splits,
                           sets=sets
                           )

@powerball.route('/trends', methods=['POST', 'GET'])
def trends():
    white_numbers_6 = [
                       1, 5, 9, 5, 6, 8, 5, 4, 3, 4, 
                       5, 3, 5, 7, 2, 9, 8, 9, 6, 4, 
                       10, 3, 3, 7, 4, 3, 8, 9, 3, 8, 
                       7, 3, 3, 3, 5, 8, 6, 6, 3, 5, 
                       6, 9, 6, 5, 3, 5, 8, 7, 6, 6, 
                       7, 10, 6, 3, 7, 10, 8, 7, 7, 9, 
                       5, 3, 10, 12, 7, 4, 3, 4, 2
                    ]

    white_numbers_trends = [
                        1, 2, 4, 2, 1, 1, 0, 1, 0, 2, 
                        0, 1, 3, 4, 1, 6, 4, 0, 1, 1, 
                        3, 1, 0, 2, 1, 2, 1, 2, 0, 3, 
                        3, 2, 0, 2, 1, 0, 2, 4, 1, 1, 
                        3, 1, 1, 5, 1, 3, 2, 4, 2, 3, 
                        1, 2, 3, 0, 3, 3, 3, 1, 3, 3, 
                        2, 1, 1, 4, 2, 3, 2, 1, 1
                    ]

    red_numbers_6 = [
                     5, 4, 4, 3, 4, 6, 1, 0, 0, 2, 
                     3, 6, 4, 7, 5, 0, 1, 2, 0, 5, 
                     2, 1, 5, 4, 2, 4
                    ]

    red_numbers_trends = [
                          0, 1, 2, 1, 0, 1, 1, 0, 0, 1, 
                          1, 4, 2, 3, 2, 0, 0, 1, 0, 2, 
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
                     6.62, 7.36, 8.26, 7.30, 6.31, 7.37, 6.37, 6.74, 6.35, 6.35, 
                     7.29, 7.48, 5.57, 6.83, 7.20, 7.82, 6.82, 7.47, 7.26, 7.44, 
                     8.87, 7.04, 8.39, 6.72, 6.20, 5.53, 8.63, 8.75, 6.60, 7.30, 
                     7.15, 8.36, 8.17, 5.83, 6.11, 8.44, 7.87, 6.74, 7.93, 7.07, 
                     6.56, 6.96, 7.48, 7.75, 7.42, 5.77, 8.03, 6.58, 5.55, 6.89, 
                     6.72, 7.57, 8.68, 6.72, 6.14, 7.15, 7.81, 6.72, 7.65, 6.42, 
                     8.74, 8.71, 8.64, 9.14, 6.11, 7.39, 7.43, 6.58, 8.78
                     ]
    red_numbers = [
                   4.02, 4.28, 4.37, 4.50, 4.64, 3.67, 3.36, 3.01, 4.03, 3.53, 
                   3.72, 3.30, 3.81, 4.95, 3.03, 2.62, 3.00, 3.75, 3.73, 4.65, 
                   4.53, 3.45, 3.51, 4.23, 4.22, 4.09
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
                     [2, 3, 19, 38, 55],
                     [6, 33, 51, 58, 64],
                     [14, 19, 37, 40, 67],
                     [15, 16, 19, 43, 59],
                     [3, 10, 21, 31, 42]
                     ]
    red_numbers = [2, 4, 15, 19, 26]
    return render_template('predictions.html',
                            draw=draw, 
                            white_numbers=white_numbers, 
                            red_numbers=red_numbers
                            )