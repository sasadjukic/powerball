

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
              'all-time': [3497, 3570, 7160],
              'six-months': [193, 203, 400],
              'recent-trends': [64, 64, 130]
            }

    sets = {
            'all-time' : [914, 1003, 1052, 1057, 997, 1040, 1097, 7160],
            'six-months' : [58, 64, 47, 48, 64, 70, 49, 400],
            'recent-trends' : [19, 20, 14, 19, 25, 23, 10, 130]
    }

    winning_hands = {
                     'singles': [236, 11, 1], 'pairs': [743, 40, 12], 
                     'two_pairs': [269, 19, 9], 'three_of_set': [152, 10, 4], 
                     'full_house': [21, 0, 0], 'poker': [11, 0, 0], 'flush': [0, 0, 0]
                     }
    total_winning_hands = sum(values[0] for values in winning_hands.values())
    total_winning_hands_6 = sum(values[1] for values in winning_hands.values())
    total_winning_hands_recent = sum(values[2] for values in winning_hands.values())

    pair_count = {
                  1: [88, 7, 3], 10: [96, 5, 0], 20: [122, 2, 1], 30: [111, 4, 3], 
                  40: [95, 8, 1], 50: [111, 9, 3], 60: [119, 5, 1]
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
              'all-time': [708, 724, 1432],
              'six-months': [42, 38, 80], 
              'recent-trends': [10, 16, 26]
            }

    sets = {
            'all-time' : [506, 518, 408, 1432],
            'six-months' : [27, 33, 20, 80],
            'recent-trends' : [6, 11, 9, 26]
           }

    return render_template('winning_hands_red.html', 
                           splits=splits,
                           sets=sets
                           )

@powerball.route('/trends', methods=['POST', 'GET'])
def trends():
    white_numbers_6 = [
                       3, 7, 9, 9, 8, 5, 4, 6, 7, 4, 
                       3, 4, 7, 10, 6, 10, 9, 6, 5, 3, 
                       8, 2, 4, 4, 5, 6, 4, 3, 8, 5, 
                       5, 6, 4, 4, 4, 6, 5, 7, 2, 6, 
                       6, 8, 3, 10, 7, 3, 4, 10, 7, 10, 
                       6, 2, 6, 6, 9, 6, 8, 9, 8, 6, 
                       5, 3, 3, 8, 6, 5, 4, 4, 5
                    ]

    white_numbers_trends = [
                        2, 1, 2, 5, 2, 1, 2, 2, 2, 0, 
                        2, 1, 4, 2, 2, 2, 2, 3, 2, 0, 
                        3, 1, 3, 1, 0, 1, 1, 1, 3, 0, 
                        2, 3, 3, 3, 2, 3, 2, 1, 0, 2, 
                        2, 5, 1, 4, 3, 1, 1, 3, 3, 3, 
                        5, 1, 1, 2, 3, 3, 3, 1, 1, 2, 
                        1, 1, 0, 1, 1, 1, 0, 1, 2
                    ]

    red_numbers_6 = [
                     2, 4, 6, 3, 3, 1, 3, 1, 4, 4, 
                     2, 4, 5, 6, 2, 1, 4, 2, 3, 5, 
                     2, 3, 5, 1, 3, 1
                    ]

    red_numbers_trends = [
                          1, 0, 0, 1, 1, 0, 1, 0, 2, 0, 
                          1, 1, 2, 1, 1, 0, 2, 0, 3, 2, 
                          2, 1, 2, 1, 1, 0
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
                     6.58, 6.79, 7.99, 7.05, 7.10, 7.62, 7.06, 6.94, 6.83, 6.18, 
                     6.92, 7.34, 5.67, 6.91, 7.11, 7.78, 6.97, 7.83, 7.56, 7.23, 
                     9.03, 6.28, 7.88, 7.01, 5.84, 6.02, 8.56, 8.41, 7.24, 7.67, 
                     7.27, 8.69, 8.27, 6.43, 6.60, 8.18, 7.51, 6.66, 7.13, 7.10, 
                     6.53, 7.04, 7.86, 7.08, 7.11, 5.67, 7.65, 6.85, 5.83, 7.58, 
                     6.62, 7.63, 7.77, 6.68, 6.82, 7.01, 7.21, 6.69, 7.63, 7.14, 
                     8.34, 8.52, 8.36, 9.23, 6.41, 6.94, 7.37, 7.18, 8.01
                ]
    red_numbers = [
                   4.66, 4.41, 3.52, 4.50, 4.26, 3.38, 3.46, 3.20, 4.30, 3.38, 
                   3.28, 3.82, 3.54, 4.92, 3.14, 2.64, 3.19, 4.35, 3.72, 4.19, 
                   4.70, 3.48, 3.77, 4.09, 4.35, 3.75
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
                     [27, 41, 56, 57, 59],
                     [8, 38, 45, 47, 69],
                     [13, 34, 37, 59, 69],
                     [25, 27, 36, 58, 62],
                     [10, 20, 44, 48, 66]
                     ]
    red_numbers = [7, 8, 15, 20, 22]
    return render_template('predictions.html',
                            draw=draw, 
                            white_numbers=white_numbers, 
                            red_numbers=red_numbers
                            )