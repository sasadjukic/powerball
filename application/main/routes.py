

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
              'all-time': [3334, 3406, 6830],
              'six-months': [185, 210, 400],
              'recent-trends': [53, 75, 130]
            }

    sets = {
            'all-time' : [863, 950, 1012, 1017, 947, 983, 1058, 6830],
            'six-months' : [48, 55, 56, 54, 59, 72, 56, 400],
            'recent-trends' : [11, 17, 12, 23, 22, 23, 22, 130]
    }

    winning_hands = {
                     'singles': [228, 15, 6], 'pairs': [710, 46, 12], 
                     'two_pairs': [254, 13, 6], 'three_of_set': [142, 4, 2], 
                     'full_house': [21, 1, 0], 'poker': [11, 1, 0], 'flush': [0, 0, 0]
                     }
    total_winning_hands = sum(values[0] for values in winning_hands.values())
    total_winning_hands_6 = sum(values[1] for values in winning_hands.values())
    total_winning_hands_recent = sum(values[2] for values in winning_hands.values())

    pair_count = {
                  1: [81, 4, 0], 10: [92, 7, 1], 20: [120, 5, 0], 30: [107, 3, 1], 
                  40: [90, 9, 4], 50: [104, 10, 3], 60: [115, 8, 3]
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
              'all-time': [674, 692, 1366],
              'six-months': [40, 40, 80], 
              'recent-trends': [14, 12, 26]
            }

    sets = {
            'all-time' : [481, 494, 391, 1366],
            'six-months' : [26, 29, 25, 80],
            'recent-trends' : [6, 15, 5, 26]
           }

    return render_template('winning_hands_red.html', 
                           splits=splits,
                           sets=sets
                           )

@powerball.route('/trends', methods=['POST', 'GET'])
def trends():
    white_numbers_6 = [
                       1, 4, 9, 7, 8, 7, 5, 4, 3, 3, 
                       7, 3, 4, 5, 2, 7, 6, 11, 7, 5, 
                       10, 3, 3, 8, 5, 2, 8, 9, 3, 7, 
                       8, 3, 3, 5, 5, 9, 6, 5, 3, 5, 
                       6, 9, 6, 4, 3, 4, 8, 8, 6, 5, 
                       7, 12, 6, 4, 7, 10, 8, 7, 6, 9, 
                       5, 4, 9, 12, 7, 3, 2, 3, 2
                    ]

    white_numbers_trends = [
                        1, 1, 4, 3, 1, 0, 0, 1, 0, 1, 
                        0, 1, 2, 2, 1, 4, 2, 2, 2, 1, 
                        2, 1, 0, 2, 2, 1, 2, 1, 0, 4, 
                        4, 2, 1, 2, 2, 3, 3, 2, 0, 1, 
                        2, 3, 1, 4, 1, 2, 2, 4, 2, 2, 
                        3, 4, 2, 0, 3, 3, 4, 1, 1, 4, 
                        2, 2, 1, 4, 4, 2, 2, 1, 0
                    ]

    red_numbers_6 = [
                     6, 4, 3, 2, 4, 5, 2, 0, 0, 2, 
                     2, 6, 4, 6, 5, 0, 1, 2, 1, 5, 
                     3, 1, 5, 4, 2, 5
                    ]

    red_numbers_trends = [
                          0, 2, 2, 0, 1, 0, 1, 0, 0, 1, 
                          0, 4, 3, 3, 3, 0, 0, 1, 0, 1, 
                          0, 1, 1, 0, 1, 1
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
                     6.83, 7.63, 8.08, 6.87, 6.29, 7.27, 7.00, 7.21, 6.50, 6.53, 
                     7.72, 7.46, 5.30, 6.55, 6.63, 7.71, 6.89, 7.84, 7.74, 6.94, 
                     9.08, 6.68, 8.69, 7.33, 6.50, 5.46, 7.92, 8.49, 6.36, 7.02, 
                     7.07, 8.64, 8.08, 6.03, 6.58, 8.36, 7.86, 6.82, 7.76, 7.32, 
                     6.29, 6.94, 7.21, 7.56, 7.36, 5.76, 8.15, 6.81, 6.16, 7.02, 
                     6.86, 7.71, 8.04, 7.32, 6.84, 6.95, 7.57, 6.89, 7.76, 6.80, 
                     8.86, 7.87, 8.18, 8.47, 6.41, 6.22, 7.54, 6.92, 8.49
                     ]
    red_numbers = [
                   3.94, 3.84, 3.96, 4.62, 4.28, 3.77, 3.12, 3.28, 4.05, 3.12, 
                   3.66, 3.62, 3.33, 4.84, 3.41, 2.59, 3.08, 4.53, 3.81, 4.38, 
                   4.69, 3.23, 3.91, 4.82, 4.16, 3.96
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
                     [3, 19, 61, 64, 68],
                     [6, 11, 20, 23, 59],
                     [13, 25, 33, 39, 60],
                     [2, 19, 57, 58, 59],
                     [7, 8, 14, 28, 39]
                     ]
    red_numbers = [2, 4, 5, 22, 24]
    return render_template('predictions.html',
                            draw=draw, 
                            white_numbers=white_numbers, 
                            red_numbers=red_numbers
                            )