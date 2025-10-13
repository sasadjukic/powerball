

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
              'all-time': [3076, 3125, 6285],
              'six-months': [201, 190, 400],
              'recent-trends': [65, 65, 130]
            }

    sets = {
            'all-time' : [797, 874, 936, 942, 872, 887, 977, 6285],
            'six-months' : [54, 56, 62, 52, 62, 50, 64, 400],
            'recent-trends' : [14, 21, 21, 11, 21, 14, 28, 130]
    }

    winning_hands = {
                     'singles': [205, 14, 2], 'pairs': [647, 39, 13], 
                     'two_pairs': [239, 15, 7], 'three_of_set': [137, 9, 3], 
                     'full_house': [19, 3, 1], 'poker': [10, 0, 0], 'flush': [0, 0, 0]
                     }
    total_winning_hands = sum(values[0] for values in winning_hands.values())
    total_winning_hands_6 = sum(values[1] for values in winning_hands.values())
    total_winning_hands_recent = sum(values[2] for values in winning_hands.values())

    pair_count = {
                  1: [76, 1, 0], 10: [82, 4, 1], 20: [115, 9, 4], 30: [102, 3, 0], 
                  40: [78, 11, 4], 50: [90, 5, 2], 60: [103, 5, 2]
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
              'all-time': [623, 634, 1257],
              'six-months': [36, 44, 80], 
              'recent-trends': [12, 14, 26]
            }

    sets = {
            'all-time' : [448, 453, 356, 1257],
            'six-months' : [28, 24, 28, 80],
            'recent-trends' : [11, 10, 5, 26]
           }

    return render_template('winning_hands_red.html', 
                           splits=splits,
                           sets=sets
                           )

@powerball.route('/trends', methods=['POST', 'GET'])
def trends():
    white_numbers_6 = [
                       6, 4, 8, 8, 4, 3, 8, 8, 5, 4, 
                       4, 5, 5, 6, 9, 10, 3, 6, 4, 4, 
                       4, 4, 10, 5, 6, 2, 6, 11, 10, 4, 
                       6, 5, 7, 7, 9, 3, 8, 1, 2, 8, 
                       3, 8, 9, 8, 8, 4, 3, 6, 5, 7, 
                       5, 8, 9, 4, 3, 2, 3, 3, 6, 5, 
                       9, 9, 5, 8, 6, 5, 7, 3, 7
                    ]

    white_numbers_trends = [
                        1, 1, 5, 1, 0, 0, 2, 3, 1, 2, 
                        3, 1, 1, 2, 4, 4, 1, 2, 1, 1, 
                        0, 3, 3, 1, 1, 1, 3, 4, 4, 1, 
                        2, 3, 1, 2, 0, 0, 2, 0, 0, 3, 
                        2, 3, 0, 3, 2, 2, 2, 1, 3, 3, 
                        1, 0, 5, 2, 1, 0, 0, 0, 2, 1, 
                        5, 3, 1, 5, 3, 3, 3, 2, 2
                    ]

    red_numbers_6 = [
                     4, 6, 3, 4, 5, 1, 0, 2, 3, 2, 
                     3, 1, 2, 3, 2, 1, 2, 2, 6, 5, 
                     4, 4, 2, 5, 8, 0
                    ]

    red_numbers_trends = [
                          2, 1, 1, 3, 3, 0, 0, 0, 1, 1, 
                          0, 0, 0, 2, 1, 1, 2, 1, 2, 1, 
                          0, 2, 1, 0, 1, 0
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
                     7.11, 7.86, 7.39, 6.60, 6.47, 6.97, 6.66, 6.82, 6.86, 7.20, 
                     7.53, 8.13, 5.61, 6.54, 7.56, 7.37, 7.49, 6.91, 7.32, 7.28, 
                     8.59, 6.76, 8.74, 7.46, 6.11, 5.54, 8.56, 8.10, 6.94, 6.38, 
                     6.45, 8.27, 8.73, 6.24, 7.13, 8.18, 8.15, 7.05, 7.78, 7.63, 
                     6.68, 6.81, 7.28, 8.29, 7.26, 6.01, 7.76, 6.10, 5.58, 6.96, 
                     6.09, 7.10, 8.11, 6.75, 6.41, 6.86, 7.19, 6.31, 7.77, 6.82, 
                     9.28, 8.37, 8.30, 8.56, 6.21, 7.17, 7.33, 7.06, 9.11
                     ]
    red_numbers = [
                   4.07, 3.50, 3.78, 4.93, 4.38, 3.63, 3.19, 3.65, 4.42, 3.51, 
                   3.46, 3.15, 3.58, 4.52, 2.94, 2.98, 3.25, 3.98, 3.95, 4.18, 
                   5.09, 3.20, 2.95, 5.15, 4.75, 3.81
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
                     [15, 31, 32, 46, 49],
                     [20, 27, 39, 43, 69],
                     [29, 33, 36, 45, 57],
                     [4, 28, 34, 42, 61],
                     [1, 21, 48, 56, 64]
                     ]
    red_numbers = [10, 14, 15, 24, 25]
    return render_template('predictions.html',
                            draw=draw, 
                            white_numbers=white_numbers, 
                            red_numbers=red_numbers
                            )