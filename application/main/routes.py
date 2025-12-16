

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
              'all-time': [3147, 3193, 6425],
              'six-months': [205, 188, 400],
              'recent-trends': [64, 65, 130]
            }

    sets = {
            'all-time' : [815, 895, 955, 962, 888, 910, 1000, 6425],
            'six-months' : [56, 58, 60, 50, 52, 54, 70, 400],
            'recent-trends' : [18, 17, 18, 18, 15, 22, 22, 130]
    }

    winning_hands = {
                     'singles': [213, 18, 8], 'pairs': [663, 39, 14], 
                     'two_pairs': [241, 13, 2], 'three_of_set': [138, 8, 1], 
                     'full_house': [20, 2, 1], 'poker': [10, 0, 0], 'flush': [0, 0, 0]
                     }
    total_winning_hands = sum(values[0] for values in winning_hands.values())
    total_winning_hands_6 = sum(values[1] for values in winning_hands.values())
    total_winning_hands_recent = sum(values[2] for values in winning_hands.values())

    pair_count = {
                  1: [77, 1, 1], 10: [85, 4, 1], 20: [115, 5, 0], 30: [104, 3, 2], 
                  40: [81, 10, 3], 50: [94, 8, 4], 60: [106, 7, 3]
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
              'all-time': [634, 651, 1285],
              'six-months': [34, 46, 80], 
              'recent-trends': [10, 16, 26]
            }

    sets = {
            'all-time' : [455, 464, 366, 1285],
            'six-months' : [27, 26, 27, 80],
            'recent-trends' : [7, 9, 10, 26]
           }

    return render_template('winning_hands_red.html', 
                           splits=splits,
                           sets=sets
                           )

@powerball.route('/trends', methods=['POST', 'GET'])
def trends():
    white_numbers_6 = [
                       4, 5, 9, 6, 3, 5, 8, 11, 5, 5, 
                       5, 5, 5, 6, 7, 9, 4, 6, 6, 2, 
                       3, 5, 8, 4, 4, 5, 6, 15, 8, 3, 
                       6, 10, 7, 5, 7, 3, 4, 2, 3, 6, 
                       2, 5, 8, 8, 4, 4, 5, 4, 6, 7, 
                       8, 7, 8, 5, 2, 1, 4, 6, 6, 5, 
                       9, 9, 4, 9, 7, 7, 7, 5, 8
                    ]

    white_numbers_trends = [
                        2, 2, 3, 1, 1, 2, 3, 3, 1, 2, 
                        1, 2, 1, 2, 1, 2, 2, 2, 2, 1, 
                        0, 2, 1, 1, 0, 4, 1, 5, 3, 2, 
                        2, 5, 2, 0, 1, 1, 1, 1, 3, 2, 
                        0, 0, 4, 3, 0, 1, 2, 1, 2, 1, 
                        5, 2, 2, 1, 0, 1, 3, 4, 3, 3, 
                        1, 2, 1, 1, 2, 4, 2, 3, 3
                    ]

    red_numbers_6 = [
                     5, 6, 3, 3, 4, 1, 1, 2, 2, 2, 
                     2, 3, 0, 4, 3, 2, 2, 3, 5, 4, 
                     3, 6, 6, 2, 4, 2
                    ]

    red_numbers_trends = [
                          3, 2, 1, 0, 0, 0, 1, 0, 0, 1, 
                          1, 1, 0, 1, 1, 1, 0, 1, 2, 1, 
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
                     7.28, 6.93, 7.41, 6.99, 5.60, 7.41, 7.40, 6.86, 6.95, 6.95, 
                     7.24, 7.40, 5.30, 6.33, 7.19, 7.45, 7.41, 7.05, 7.55, 7.02, 
                     9.14, 6.63, 8.82, 7.30, 6.38, 5.87, 9.06, 8.32, 7.06, 7.54, 
                     6.85, 8.74, 8.40, 6.11, 6.20, 8.07, 8.22, 6.30, 7.48, 7.40, 
                     6.30, 6.86, 7.28, 8.46, 7.52, 5.96, 8.09, 6.27, 6.21, 7.31, 
                     6.35, 7.41, 8.26, 6.93, 6.21, 6.73, 6.72, 6.81, 8.37, 6.35, 
                     9.40, 8.22, 7.49, 7.80, 6.23, 7.63, 7.67, 6.90, 8.65
                     ]
    red_numbers = [
                   3.71, 3.43, 3.62, 4.87, 4.05, 3.34, 3.48, 3.43, 4.17, 3.88, 
                   3.47, 3.25, 3.97, 4.81, 3.33, 3.35, 3.22, 4.47, 3.77, 4.29, 
                   4.56, 3.51, 3.53, 4.45, 4.21, 3.83
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
                     [3, 7, 15, 24, 60],
                     [2, 9, 21, 40, 63],
                     [1, 23, 37, 50, 54],
                     [11, 13, 31, 39, 44],
                     [28, 61, 62, 64, 68]
                     ]
    red_numbers = [3, 4, 6, 22, 26]
    return render_template('predictions.html',
                            draw=draw, 
                            white_numbers=white_numbers, 
                            red_numbers=red_numbers
                            )