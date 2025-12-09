

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
              'all-time': [3139, 3187, 6410],
              'six-months': [203, 191, 400],
              'recent-trends': [68, 62, 130]
            }

    sets = {
            'all-time' : [814, 893, 952, 959, 888, 907, 997, 6410],
            'six-months' : [55, 57, 59, 52, 56, 53, 68, 400],
            'recent-trends' : [17, 22, 18, 17, 16, 20, 20, 130]
    }

    winning_hands = {
                     'singles': [213, 18, 8], 'pairs': [660, 37, 13], 
                     'two_pairs': [241, 15, 2], 'three_of_set': [138, 8, 1], 
                     'full_house': [20, 2, 2], 'poker': [10, 0, 0], 'flush': [0, 0, 0]
                     }
    total_winning_hands = sum(values[0] for values in winning_hands.values())
    total_winning_hands_6 = sum(values[1] for values in winning_hands.values())
    total_winning_hands_recent = sum(values[2] for values in winning_hands.values())

    pair_count = {
                  1: [77, 1, 1], 10: [84, 3, 2], 20: [115, 6, 0], 30: [104, 3, 2], 
                  40: [81, 10, 3], 50: [93, 7, 3], 60: [105, 6, 2]
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
              'all-time': [633, 649, 1282],
              'six-months': [34, 46, 80], 
              'recent-trends': [11, 15, 26]
            }

    sets = {
            'all-time' : [454, 463, 365, 1282],
            'six-months' : [27, 25, 28, 80],
            'recent-trends' : [6, 11, 9, 26]
           }

    return render_template('winning_hands_red.html', 
                           splits=splits,
                           sets=sets
                           )

@powerball.route('/trends', methods=['POST', 'GET'])
def trends():
    white_numbers_6 = [
                       3, 5, 9, 6, 3, 5, 8, 11, 5, 4, 
                       5, 5, 6, 6, 7, 8, 4, 6, 6, 2, 
                       3, 5, 7, 4, 5, 5, 6, 14, 8, 4, 
                       6, 10, 7, 5, 6, 4, 5, 2, 3, 7, 
                       2, 5, 10, 8, 4, 4, 5, 5, 6, 7, 
                       8, 8, 9, 5, 2, 1, 3, 5, 5, 5, 
                       9, 10, 3, 9, 7, 7, 7, 4, 7
                    ]

    white_numbers_trends = [
                        1, 2, 3, 1, 1, 2, 3, 3, 1, 2, 
                        1, 2, 4, 3, 1, 2, 2, 3, 2, 2, 
                        0, 2, 0, 1, 0, 4, 2, 5, 2, 2, 
                        1, 6, 1, 1, 0, 1, 1, 1, 3, 2, 
                        0, 0, 4, 3, 0, 1, 3, 1, 2, 1, 
                        5, 3, 2, 1, 0, 1, 2, 3, 2, 3, 
                        1, 2, 0, 2, 2, 4, 2, 2, 2
                    ]

    red_numbers_6 = [
                     5, 5, 4, 3, 4, 1, 1, 2, 2, 2, 
                     2, 3, 0, 4, 3, 1, 2, 3, 5, 4, 
                     3, 5, 6, 2, 6, 2
                    ]

    red_numbers_trends = [
                          3, 1, 1, 0, 0, 0, 1, 0, 0, 2, 
                          1, 2, 0, 1, 2, 0, 0, 1, 2, 1, 
                          1, 1, 4, 0, 0, 2
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
                     6.96, 7.41, 7.56, 6.90, 5.87, 7.55, 7.25, 6.85, 6.59, 6.48, 
                     7.23, 8.25, 5.25, 6.47, 7.42, 7.63, 7.07, 6.81, 7.37, 7.34, 
                     8.62, 6.90, 9.38, 7.08, 6.42, 6.40, 7.62, 8.39, 6.23, 6.93, 
                     6.39, 8.88, 8.43, 6.14, 6.40, 7.43, 8.37, 6.73, 7.51, 7.35, 
                     6.42, 7.04, 7.25, 7.73, 7.54, 6.26, 7.92, 6.79, 5.53, 7.19, 
                     6.29, 7.85, 8.08, 7.18, 6.38, 6.95, 6.96, 6.78, 7.89, 6.70, 
                     8.71, 8.33, 8.05, 8.44, 6.66, 7.66, 7.57, 7.61, 8.38
                     ]
    red_numbers = [
                   4.23, 3.77, 4.08, 5.24, 3.92, 3.46, 3.41, 3.93, 3.99, 3.46, 
                   3.36, 3.15, 3.85, 4.81, 3.26, 2.59, 3.09, 4.08, 3.92, 4.19, 
                   4.48, 3.36, 3.52, 4.58, 4.23, 4.04
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
                     [29, 36, 37, 41, 52],
                     [5, 14, 21, 25, 66],
                     [15, 20, 22, 32, 67],
                     [2, 10, 28, 53, 64],
                     [1, 16, 30, 46, 61]
                     ]
    red_numbers = [1, 8, 13, 21, 26]
    return render_template('predictions.html',
                            draw=draw, 
                            white_numbers=white_numbers, 
                            red_numbers=red_numbers
                            )