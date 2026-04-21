

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
              'all-time': [3278, 3329, 6695],
              'six-months': [195, 201, 400],
              'recent-trends': [59, 70, 130]
            }

    sets = {
            'all-time' : [852, 933, 998, 993, 924, 960, 1035, 6695],
            'six-months' : [55, 55, 61, 49, 51, 72, 57, 400],
            'recent-trends' : [17, 22, 17, 12, 22, 24, 16, 130]
    }

    winning_hands = {
                     'singles': [222, 17, 6], 'pairs': [697, 48, 14], 
                     'two_pairs': [248, 9, 3], 'three_of_set': [140, 3, 2], 
                     'full_house': [21, 2, 0], 'poker': [11, 1, 1], 'flush': [0, 0, 0]
                     }
    total_winning_hands = sum(values[0] for values in winning_hands.values())
    total_winning_hands_6 = sum(values[1] for values in winning_hands.values())
    total_winning_hands_recent = sum(values[2] for values in winning_hands.values())

    pair_count = {
                  1: [81, 5, 1], 10: [91, 7, 5], 20: [119, 4, 2], 30: [106, 4, 0], 
                  40: [86, 8, 3], 50: [101, 11, 2], 60: [112, 9, 1]
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
              'all-time': [659, 680, 1339],
              'six-months': [35, 45, 80], 
              'recent-trends': [13, 13, 26]
            }

    sets = {
            'all-time' : [475, 478, 386, 1339],
            'six-months' : [27, 23, 30, 80],
            'recent-trends' : [10, 4, 12, 26]
           }

    return render_template('winning_hands_red.html', 
                           splits=splits,
                           sets=sets
                           )

@powerball.route('/trends', methods=['POST', 'GET'])
def trends():
    white_numbers_6 = [
                       2, 5, 8, 5, 8, 9, 8, 6, 4, 4, 
                       8, 4, 3, 5, 2, 5, 6, 11, 7, 5, 
                       8, 4, 4, 6, 4, 5, 7, 13, 5, 5, 
                       6, 5, 5, 3, 4, 7, 4, 4, 6, 6, 
                       4, 6, 9, 3, 2, 3, 8, 5, 5, 4, 
                       9, 10, 7, 5, 4, 8, 7, 10, 8, 8, 
                       4, 5, 8, 9, 5, 6, 2, 5, 5
                    ]

    white_numbers_trends = [
                        0, 1, 3, 1, 1, 4, 5, 0, 2, 2, 
                        4, 2, 2, 2, 0, 1, 4, 4, 1, 2, 
                        3, 1, 2, 2, 1, 0, 2, 3, 1, 2, 
                        1, 0, 0, 0, 1, 4, 1, 2, 1, 0, 
                        3, 5, 3, 0, 1, 1, 6, 1, 2, 3, 
                        0, 5, 1, 3, 2, 4, 2, 1, 3, 1, 
                        2, 1, 3, 5, 2, 0, 0, 1, 1
                    ]

    red_numbers_6 = [
                     9, 4, 2, 2, 3, 5, 2, 0, 0, 2, 
                     2, 3, 1, 4, 3, 1, 2, 2, 3, 5, 
                     4, 2, 8, 4, 1, 6
                    ]

    red_numbers_trends = [
                          4, 1, 1, 0, 1, 3, 0, 0, 0, 1, 
                          0, 1, 1, 0, 1, 0, 0, 0, 0, 3, 
                          2, 0, 1, 2, 1, 3
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
                     6.17, 7.38, 8.01, 7.16, 6.62, 7.58, 6.83, 7.17, 6.92, 6.69, 
                     6.77, 7.49, 5.65, 6.41, 6.64, 7.19, 7.30, 7.22, 7.73, 6.93, 
                     8.86, 6.63, 8.59, 7.11, 6.81, 5.64, 8.46, 9.00, 6.16, 6.83, 
                     7.20, 8.47, 8.77, 6.06, 5.94, 8.30, 7.71, 6.38, 7.72, 7.34, 
                     6.66, 6.97, 7.30, 7.59, 7.38, 5.47, 8.22, 6.61, 6.27, 7.06, 
                     6.82, 8.06, 8.50, 7.33, 6.43, 6.95, 6.83, 7.01, 7.47, 6.65, 
                     8.57, 8.34, 9.20, 8.87, 6.18, 7.25, 6.91, 6.83, 8.43
                     ]
    red_numbers = [
                   4.38, 3.78, 3.97, 4.73, 4.46, 3.94, 3.15, 3.56, 4.10, 3.67, 
                   3.30, 3.51, 3.52, 4.43, 2.87, 2.98, 3.36, 4.47, 3.58, 4.50, 
                   4.38, 3.18, 3.15, 4.67, 4.20, 4.16
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
                     [1, 21, 24, 37, 65],
                     [10, 17, 28, 44, 50],
                     [2, 11, 16, 17, 24],
                     [4, 31, 47, 49, 64],
                     [27, 32, 33, 40, 44]
                     ]
    red_numbers = [3, 10, 19, 22, 23]
    return render_template('predictions.html',
                            draw=draw, 
                            white_numbers=white_numbers, 
                            red_numbers=red_numbers
                            )