

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
              'all-time': [3235, 3277, 6600],
              'six-months': [202, 194, 400],
              'recent-trends': [63, 64, 130]
            }

    sets = {
            'all-time' : [839, 917, 986, 985, 907, 943, 1023, 6600],
            'six-months' : [52, 56, 65, 49, 48, 66, 64, 400],
            'recent-trends' : [18, 15, 23, 16, 16, 24, 18, 130]
    }

    winning_hands = {
                     'singles': [217, 13, 2], 'pairs': [687, 49, 18], 
                     'two_pairs': [246, 12, 4], 'three_of_set': [138, 2, 0], 
                     'full_house': [21, 3, 1], 'poker': [11, 1, 1], 'flush': [0, 0, 0]
                     }
    total_winning_hands = sum(values[0] for values in winning_hands.values())
    total_winning_hands_6 = sum(values[1] for values in winning_hands.values())
    total_winning_hands_recent = sum(values[2] for values in winning_hands.values())

    pair_count = {
                  1: [80, 4, 2], 10: [88, 6, 2], 20: [118, 5, 3], 30: [106, 4, 1], 
                  40: [84, 9, 3], 50: [99, 11, 3], 60: [111, 10, 4]
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
              'all-time': [649, 671, 1320],
              'six-months': [34, 46, 80], 
              'recent-trends': [13, 13, 26]
            }

    sets = {
            'all-time' : [467, 475, 378, 1320],
            'six-months' : [26, 30, 24, 80],
            'recent-trends' : [10, 8, 8, 26]
           }

    return render_template('winning_hands_red.html', 
                           splits=splits,
                           sets=sets
                           )

@powerball.route('/trends', methods=['POST', 'GET'])
def trends():
    white_numbers_6 = [
                       3, 6, 9, 4, 8, 6, 6, 8, 2, 5, 
                       6, 2, 4, 6, 5, 7, 5, 10, 6, 5, 
                       5, 4, 4, 5, 3, 6, 8, 16, 9, 5, 
                       6, 9, 5, 4, 4, 4, 4, 3, 5, 6, 
                       2, 5, 6, 5, 3, 3, 6, 6, 6, 5, 
                       9, 7, 10, 6, 3, 6, 5, 9, 6, 8, 
                       5, 7, 5, 9, 5, 9, 5, 6, 5
                    ]

    white_numbers_trends = [
                        0, 3, 1, 0, 5, 4, 1, 3, 1, 0, 
                        2, 0, 0, 2, 1, 2, 2, 3, 3, 2, 
                        3, 1, 2, 1, 1, 1, 5, 5, 2, 2, 
                        2, 0, 2, 1, 3, 2, 2, 1, 1, 3, 
                        0, 2, 2, 0, 1, 1, 2, 3, 2, 2, 
                        3, 2, 1, 2, 2, 4, 2, 5, 1, 3, 
                        1, 1, 4, 4, 2, 1, 0, 2, 0
                    ]

    red_numbers_6 = [
                     6, 4, 2, 4, 3, 4, 2, 0, 1, 3, 
                     2, 3, 0, 6, 4, 2, 3, 2, 5, 4, 
                     3, 3, 8, 3, 0, 3
                    ]

    red_numbers_trends = [
                          1, 1, 0, 2, 2, 4, 0, 0, 0, 1, 
                          1, 1, 0, 2, 1, 0, 1, 1, 0, 1, 
                          1, 0, 3, 3, 0, 0
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
                     7.10, 7.27, 7.53, 7.12, 6.92, 8.25, 6.38, 6.91, 6.82, 6.90, 
                     7.33, 7.69, 4.77, 6.48, 6.98, 7.68, 6.83, 7.14, 7.42, 7.48, 
                     9.05, 6.62, 8.87, 7.23, 6.34, 5.54, 8.25, 8.78, 6.55, 7.02, 
                     6.99, 8.56, 9.01, 6.18, 6.84, 8.51, 8.33, 6.25, 8.52, 7.25, 
                     6.24, 6.55, 7.18, 7.80, 7.45, 5.90, 7.24, 6.23, 6.16, 7.17, 
                     6.77, 8.01, 7.96, 7.26, 6.38, 6.77, 6.83, 7.10, 7.59, 6.34, 
                     9.18, 8.21, 8.10, 7.91, 6.30, 6.81, 7.81, 7.02, 8.04
                     ]
    red_numbers = [
                   4.21, 3.79, 3.71, 4.83, 4.25, 3.94, 2.96, 3.44, 4.36, 3.31, 
                   3.44, 3.22, 3.69, 4.35, 3.22, 3.21, 3.28, 4.72, 3.38, 4.48, 
                   4.57, 3.22, 3.45, 4.87, 4.34, 3.76
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
                     [12, 15, 19, 25, 67],
                     [9, 29, 54, 56, 66],
                     [17, 32, 38, 43, 55],
                     [3, 6, 22, 41, 61],
                     [1, 2, 5, 39, 51]
                     ]
    red_numbers = [2, 3, 4, 6, 19]
    return render_template('predictions.html',
                            draw=draw, 
                            white_numbers=white_numbers, 
                            red_numbers=red_numbers
                            )