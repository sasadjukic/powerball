

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
              'all-time': [3160, 3205, 6450],
              'six-months': [203, 190, 400],
              'recent-trends': [68, 61, 130]
            }

    sets = {
            'all-time' : [820, 896, 959, 967, 889, 915, 1004, 6450],
            'six-months' : [56, 57, 57, 54, 51, 55, 70, 400],
            'recent-trends' : [21, 14, 20, 18, 14, 23, 20, 130]
    }

    winning_hands = {
                     'singles': [214, 18, 6], 'pairs': [667, 42, 17], 
                     'two_pairs': [241, 12, 2], 'three_of_set': [138, 6, 1], 
                     'full_house': [20, 2, 0], 'poker': [10, 0, 0], 'flush': [0, 0, 0]
                     }
    total_winning_hands = sum(values[0] for values in winning_hands.values())
    total_winning_hands_6 = sum(values[1] for values in winning_hands.values())
    total_winning_hands_recent = sum(values[2] for values in winning_hands.values())

    pair_count = {
                  1: [78, 2, 2], 10: [85, 4, 1], 20: [115, 5, 0], 30: [105, 4, 3], 
                  40: [81, 9, 3], 50: [95, 9, 4], 60: [107, 8, 4]
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
              'all-time': [636, 654, 1290],
              'six-months': [35, 45, 80], 
              'recent-trends': [10, 16, 26]
            }

    sets = {
            'all-time' : [457, 466, 367, 1290],
            'six-months' : [29, 26, 25, 80],
            'recent-trends' : [9, 7, 10, 26]
           }

    return render_template('winning_hands_red.html', 
                           splits=splits,
                           sets=sets
                           )

@powerball.route('/trends', methods=['POST', 'GET'])
def trends():
    white_numbers_6 = [
                       4, 5, 9, 7, 4, 4, 8, 11, 4, 5, 
                       5, 5, 5, 6, 7, 8, 3, 7, 6, 3, 
                       2, 5, 5, 4, 5, 5, 5, 16, 7, 3, 
                       7, 9, 8, 6, 7, 4, 4, 2, 4, 6, 
                       3, 4, 8, 7, 4, 4, 5, 4, 6, 6, 
                       8, 7, 9, 6, 2, 1, 4, 6, 6, 5, 
                       9, 10, 4, 8, 6, 8, 6, 5, 9
                    ]

    white_numbers_trends = [
                        2, 1, 3, 3, 3, 2, 3, 3, 1, 2, 
                        0, 1, 1, 2, 1, 2, 1, 2, 2, 2, 
                        0, 1, 1, 1, 2, 4, 0, 6, 3, 2, 
                        3, 4, 3, 1, 1, 2, 0, 0, 2, 1, 
                        1, 0, 3, 3, 0, 1, 2, 1, 2, 1, 
                        4, 3, 3, 1, 0, 1, 3, 3, 4, 2, 
                        1, 4, 1, 1, 2, 3, 0, 3, 3
                    ]

    red_numbers_6 = [
                     6, 6, 3, 3, 4, 1, 2, 2, 2, 2, 
                     1, 3, 0, 4, 3, 2, 3, 3, 5, 4, 
                     3, 6, 6, 1, 3, 2
                    ]

    red_numbers_trends = [
                          4, 2, 1, 0, 0, 0, 2, 0, 0, 0, 
                          1, 0, 0, 1, 0, 1, 1, 1, 2, 1, 
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
                     7.30, 7.57, 7.39, 6.84, 6.81, 7.52, 6.76, 6.57, 6.51, 7.03, 
                     6.95, 7.73, 5.13, 6.82, 6.28, 7.26, 7.53, 7.25, 7.57, 7.78, 
                     8.93, 7.60, 8.73, 7.32, 6.52, 5.34, 7.96, 8.47, 7.21, 6.82, 
                     6.87, 8.43, 8.73, 6.29, 6.67, 8.08, 7.91, 6.72, 8.06, 7.29, 
                     5.69, 6.41, 7.18, 7.93, 7.46, 5.93, 8.11, 6.51, 5.53, 6.78, 
                     6.72, 7.43, 7.72, 7.27, 6.61, 6.92, 6.63, 6.30, 8.56, 6.01, 
                     9.45, 8.31, 8.41, 8.38, 6.45, 7.33, 7.38, 7.11, 8.93
                     ]
    red_numbers = [
                   3.89, 3.75, 4.06, 4.72, 4.32, 3.40, 3.36, 3.31, 4.15, 3.34, 
                   3.38, 3.31, 3.83, 4.24, 3.24, 2.96, 3.43, 4.41, 3.96, 4.31, 
                   4.72, 3.71, 3.13, 4.42, 4.49, 4.16
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
                     [28, 32, 54, 55, 58],
                     [8, 15, 34, 47, 50],
                     [1, 9, 21, 26, 27],
                     [2, 6, 52, 56, 67],
                     [4, 5, 19, 29, 53]
                     ]
    red_numbers = [4, 5, 8, 13, 23]
    return render_template('predictions.html',
                            draw=draw, 
                            white_numbers=white_numbers, 
                            red_numbers=red_numbers
                            )