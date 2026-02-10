

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
              'all-time': [3210, 3248, 6545],
              'six-months': [206, 191, 400],
              'recent-trends': [67, 60, 130]
            }

    sets = {
            'all-time' : [833, 908, 979, 979, 899, 932, 1015, 6545],
            'six-months' : [52, 57, 66, 49, 49, 59, 68, 400],
            'recent-trends' : [19, 13, 26, 19, 11, 25, 17, 130]
    }

    winning_hands = {
                     'singles': [216, 14, 3], 'pairs': [680, 47, 19], 
                     'two_pairs': [245, 13, 4], 'three_of_set': [138, 4, 0], 
                     'full_house': [20, 2, 0], 'poker': [10, 0, 0], 'flush': [0, 0, 0]
                     }
    total_winning_hands = sum(values[0] for values in winning_hands.values())
    total_winning_hands_6 = sum(values[1] for values in winning_hands.values())
    total_winning_hands_recent = sum(values[2] for values in winning_hands.values())

    pair_count = {
                  1: [80, 4, 3], 10: [86, 5, 2], 20: [117, 7, 2], 30: [106, 4, 2], 
                  40: [82, 8, 1], 50: [99, 11, 6], 60: [109, 8, 4]
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
              'all-time': [643, 666, 1309],
              'six-months': [33, 47, 80], 
              'recent-trends': [10, 16, 26]
            }

    sets = {
            'all-time' : [462, 474, 373, 1309],
            'six-months' : [26, 32, 22, 80],
            'recent-trends' : [8, 11, 7, 26]
           }

    return render_template('winning_hands_red.html', 
                           splits=splits,
                           sets=sets
                           )

@powerball.route('/trends', methods=['POST', 'GET'])
def trends():
    white_numbers_6 = [
                       3, 5, 10, 5, 7, 5, 6, 9, 2, 5, 
                       7, 3, 4, 7, 6, 8, 3, 8, 6, 3, 
                       5, 6, 5, 6, 4, 6, 8, 15, 8, 4, 
                       7, 9, 5, 6, 3, 3, 5, 2, 5, 9, 
                       3, 4, 5, 6, 3, 4, 5, 4, 6, 4, 
                       10, 5, 11, 4, 3, 3, 5, 7, 7, 8, 
                       7, 8, 6, 8, 6, 8, 5, 6, 6
                    ]

    white_numbers_trends = [
                        1, 2, 2, 3, 6, 2, 0, 3, 0, 0, 
                        3, 0, 0, 1, 1, 1, 0, 4, 3, 1, 
                        5, 1, 1, 3, 3, 1, 4, 6, 1, 1, 
                        4, 0, 1, 3, 3, 2, 2, 1, 2, 3, 
                        1, 1, 1, 0, 1, 1, 0, 2, 1, 0, 
                        4, 2, 4, 1, 2, 2, 3, 4, 3, 3, 
                        1, 2, 5, 1, 1, 1, 0, 2, 1
                    ]

    red_numbers_6 = [
                     6, 5, 2, 5, 4, 1, 2, 0, 1, 2, 
                     2, 3, 0, 7, 4, 2, 4, 3, 5, 3, 
                     2, 4, 8, 1, 1, 3
                    ]

    red_numbers_trends = [
                          1, 2, 0, 2, 1, 1, 1, 0, 0, 0, 
                          1, 1, 0, 3, 1, 1, 2, 1, 1, 1, 
                          1, 0, 3, 1, 0, 1
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
                     6.88, 6.58, 8.02, 7.00, 6.53, 7.12, 6.77, 6.79, 6.74, 6.83, 
                     7.32, 7.83, 5.50, 6.40, 6.94, 7.78, 6.45, 7.32, 7.33, 7.42, 
                     9.18, 7.08, 8.51, 7.11, 6.41, 6.11, 8.53, 8.56, 6.57, 7.56, 
                     7.36, 9.04, 8.40, 6.83, 6.81, 8.20, 8.06, 6.77, 8.13, 6.85, 
                     6.27, 6.95, 7.23, 7.71, 7.49, 5.88, 7.83, 6.93, 5.48, 6.35, 
                     6.52, 7.37, 7.97, 7.24, 6.37, 6.35, 6.85, 6.66, 7.77, 6.85, 
                     9.24, 8.01, 7.82, 8.60, 6.32, 7.78, 7.11, 7.15, 8.28
                     ]
    red_numbers = [
                   4.08, 3.89, 3.93, 4.72, 3.56, 3.54, 3.33, 3.27, 3.88, 3.73, 
                   3.46, 3.26, 3.52, 4.88, 3.23, 3.12, 3.01, 4.59, 3.99, 4.29, 
                   4.76, 3.38, 3.69, 4.53, 4.47, 3.89
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
                     [5, 15, 24, 36, 56],
                     [23, 26, 28, 40, 57],
                     [1, 6, 8, 30, 61],
                     [9, 44, 49, 59, 63],
                     [10, 27, 42, 53, 54]
                     ]
    red_numbers = [2, 10, 17, 19, 25]
    return render_template('predictions.html',
                            draw=draw, 
                            white_numbers=white_numbers, 
                            red_numbers=red_numbers
                            )