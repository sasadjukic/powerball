

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
              'all-time': [3163, 3207, 6455],
              'six-months': [204, 189, 400],
              'recent-trends': [69, 60, 130]
            }

    sets = {
            'all-time' : [820, 898, 959, 968, 890, 916, 1004, 6455],
            'six-months' : [55, 58, 57, 54, 52, 55, 69, 400],
            'recent-trends' : [20, 16, 19, 19, 14, 24, 18, 130]
    }

    winning_hands = {
                     'singles': [214, 17, 6], 'pairs': [668, 43, 17], 
                     'two_pairs': [241, 12, 2], 'three_of_set': [138, 6, 1], 
                     'full_house': [20, 2, 0], 'poker': [10, 0, 0], 'flush': [0, 0, 0]
                     }
    total_winning_hands = sum(values[0] for values in winning_hands.values())
    total_winning_hands_6 = sum(values[1] for values in winning_hands.values())
    total_winning_hands_recent = sum(values[2] for values in winning_hands.values())

    pair_count = {
                  1: [78, 2, 2], 10: [86, 5, 2], 20: [115, 5, 0], 30: [105, 4, 3], 
                  40: [81, 9, 3], 50: [95, 9, 4], 60: [107, 8, 3]
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
              'all-time': [636, 655, 1291],
              'six-months': [35, 45, 80], 
              'recent-trends': [9, 17, 26]
            }

    sets = {
            'all-time' : [457, 466, 368, 1291],
            'six-months' : [29, 26, 25, 80],
            'recent-trends' : [8, 7, 11, 26]
           }

    return render_template('winning_hands_red.html', 
                           splits=splits,
                           sets=sets
                           )

@powerball.route('/trends', methods=['POST', 'GET'])
def trends():
    white_numbers_6 = [
                       4, 4, 9, 7, 4, 4, 8, 11, 4, 5, 
                       6, 4, 5, 6, 7, 8, 3, 7, 7, 3, 
                       2, 5, 5, 4, 5, 5, 5, 16, 7, 3, 
                       7, 9, 8, 7, 7, 4, 3, 2, 4, 6, 
                       3, 4, 8, 7, 4, 4, 5, 5, 6, 6, 
                       7, 7, 10, 6, 2, 1, 4, 6, 6, 5, 
                       8, 10, 4, 8, 6, 8, 6, 5, 9
                    ]

    white_numbers_trends = [
                        2, 1, 3, 2, 3, 2, 3, 3, 1, 2, 
                        1, 1, 1, 2, 1, 2, 1, 2, 3, 2, 
                        0, 1, 1, 0, 2, 4, 0, 6, 3, 2, 
                        3, 4, 3, 2, 1, 2, 0, 0, 2, 1, 
                        1, 0, 3, 3, 0, 1, 2, 2, 1, 1, 
                        4, 3, 4, 1, 0, 1, 3, 3, 4, 1, 
                        1, 4, 1, 1, 1, 3, 0, 3, 3
                    ]

    red_numbers_6 = [
                     6, 6, 3, 3, 4, 1, 2, 2, 2, 2, 
                     1, 3, 0, 4, 3, 2, 3, 3, 5, 4, 
                     4, 5, 6, 1, 3, 2
                    ]

    red_numbers_trends = [
                          3, 2, 1, 0, 0, 0, 2, 0, 0, 0, 
                          1, 0, 0, 1, 0, 1, 1, 1, 2, 1, 
                          2, 2, 4, 0, 0, 2
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
                     7.26, 7.30, 8.29, 6.52, 6.30, 7.91, 6.35, 7.28, 6.39, 6.14, 
                     7.57, 8.04, 5.52, 6.67, 7.10, 7.47, 6.66, 7.32, 7.22, 7.18, 
                     8.70, 6.92, 8.46, 7.06, 6.32, 5.72, 8.59, 8.52, 6.68, 7.13, 
                     6.94, 8.73, 8.67, 6.49, 6.55, 8.05, 8.34, 6.69, 7.82, 7.28, 
                     6.47, 6.43, 7.16, 8.01, 7.45, 5.53, 7.34, 6.13, 5.65, 7.65, 
                     6.91, 7.51, 8.20, 6.95, 6.83, 6.58, 7.04, 6.57, 7.79, 6.48, 
                     9.20, 8.24, 8.55, 8.60, 6.11, 7.50, 7.35, 7.44, 8.18
                     ]
    red_numbers = [
                   4.38, 3.69, 4.00, 4.99, 4.16, 3.64, 3.65, 3.39, 3.92, 3.49, 
                   3.33, 3.21, 3.62, 4.63, 3.08, 2.98, 3.40, 4.20, 3.57, 4.46, 
                   4.50, 3.48, 3.60, 4.65, 4.12, 3.86
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
                     [17, 20, 30, 65, 69],
                     [22, 44, 45, 55, 61],
                     [6, 32, 37, 38, 67],
                     [7, 28, 31, 46, 54],
                     [1, 29, 35, 36, 57]
                     ]
    red_numbers = [3, 4, 11, 14, 26]
    return render_template('predictions.html',
                            draw=draw, 
                            white_numbers=white_numbers, 
                            red_numbers=red_numbers
                            )