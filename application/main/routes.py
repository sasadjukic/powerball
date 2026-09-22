

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
              'all-time': [3428, 3506, 7025],
              'six-months': [179, 218, 400],
              'recent-trends': [61, 68, 130]
            }

    sets = {
            'all-time' : [894, 982, 1036, 1037, 972, 1017, 1087, 7025],
            'six-months' : [51, 61, 45, 50, 63, 68, 62, 400],
            'recent-trends' : [19, 19, 17, 13, 16, 22, 24, 130]
    }

    winning_hands = {
                     'singles': [235, 17, 4], 'pairs': [730, 42, 15], 
                     'two_pairs': [260, 13, 3], 'three_of_set': [148, 8, 4], 
                     'full_house': [21, 0, 0], 'poker': [11, 0, 0], 'flush': [0, 0, 0]
                     }
    total_winning_hands = sum(values[0] for values in winning_hands.values())
    total_winning_hands_6 = sum(values[1] for values in winning_hands.values())
    total_winning_hands_recent = sum(values[2] for values in winning_hands.values())

    pair_count = {
                  1: [85, 5, 2], 10: [96, 8, 3], 20: [120, 2, 0], 30: [108, 2, 1], 
                  40: [94, 10, 3], 50: [108, 8, 3], 60: [118, 7, 3]
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
              'all-time': [698, 707, 1405],
              'six-months': [46, 34, 80], 
              'recent-trends': [15, 11, 26]
            }

    sets = {
            'all-time' : [500, 506, 399, 1405],
            'six-months' : [32, 29, 19, 80],
            'recent-trends' : [11, 8, 7, 26]
           }

    return render_template('winning_hands_red.html', 
                           splits=splits,
                           sets=sets
                           )

@powerball.route('/trends', methods=['POST', 'GET'])
def trends():
    white_numbers_6 = [
                       1, 6, 10, 7, 5, 6, 5, 5, 6, 6, 
                       4, 5, 6, 8, 4, 9, 9, 6, 4, 3, 
                       7, 2, 1, 7, 7, 4, 5, 4, 5, 8, 
                       6, 4, 2, 2, 3, 8, 7, 7, 3, 5, 
                       8, 8, 5, 7, 5, 5, 7, 7, 6, 7, 
                       3, 6, 6, 4, 7, 8, 9, 8, 10, 6, 
                       7, 3, 7, 12, 10, 4, 6, 4, 3
                    ]

    white_numbers_trends = [
                        0, 2, 3, 2, 2, 3, 1, 3, 3, 2, 
                        1, 1, 1, 2, 3, 2, 3, 2, 2, 2, 
                        2, 0, 1, 2, 3, 2, 2, 1, 2, 3, 
                        1, 1, 1, 0, 1, 2, 2, 1, 1, 3, 
                        2, 2, 0, 0, 2, 1, 2, 2, 2, 2, 
                        0, 0, 1, 4, 2, 2, 3, 6, 2, 1, 
                        3, 1, 2, 4, 5, 1, 3, 2, 2
                    ]

    red_numbers_6 = [
                     4, 6, 8, 2, 4, 2, 3, 1, 2, 4, 
                     2, 4, 4, 5, 4, 1, 2, 3, 0, 4, 
                     0, 3, 3, 1, 4, 4
                    ]

    red_numbers_trends = [
                          0, 3, 2, 1, 1, 0, 2, 0, 2, 3, 
                          0, 0, 1, 1, 0, 0, 2, 1, 0, 1, 
                          0, 2, 2, 0, 2, 0
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
                     6.99, 7.15, 8.24, 6.95, 6.67, 7.43, 7.04, 6.65, 6.56, 7.04, 
                     7.08, 7.16, 5.24, 6.73, 6.33, 7.65, 7.27, 7.84, 6.94, 7.20, 
                     8.61, 6.51, 8.24, 6.93, 6.65, 5.81, 8.64, 8.22, 6.52, 7.58, 
                     7.25, 8.01, 7.61, 6.22, 6.37, 8.53, 7.83, 7.11, 8.04, 7.38, 
                     6.36, 6.59, 7.10, 7.96, 6.88, 6.13, 7.88, 6.16, 5.62, 7.32, 
                     6.77, 7.17, 7.95, 7.51, 6.12, 7.33, 7.23, 6.62, 8.22, 7.07, 
                     8.98, 8.59, 8.48, 8.67, 6.60, 7.19, 7.41, 7.59, 8.28
                ]
    red_numbers = [
                   4.26, 4.06, 4.10, 4.70, 4.33, 3.53, 3.58, 2.93, 3.96, 3.51, 
                   3.38, 3.59, 3.70, 5.01, 3.38, 2.92, 3.19, 4.30, 3.51, 4.49, 
                   4.47, 3.22, 3.63, 4.33, 4.20, 3.72
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
                     [11, 24, 25, 26, 31],
                     [13, 32, 39, 51, 63],
                     [8, 35, 45, 48, 64],
                     [12, 17, 21, 28, 45],
                     [3, 25, 28, 33, 45]
                     ]
    red_numbers = [6, 8, 12, 13, 24]
    return render_template('predictions.html',
                            draw=draw, 
                            white_numbers=white_numbers, 
                            red_numbers=red_numbers
                            )