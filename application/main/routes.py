

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
              'all-time': [3324, 3391, 6805],
              'six-months': [187, 207, 400],
              'recent-trends': [53, 75, 130]
            }

    sets = {
            'all-time' : [861, 946, 1008, 1017, 941, 977, 1055, 6805],
            'six-months' : [48, 53, 56, 59, 53, 72, 59, 400],
            'recent-trends' : [10, 15, 14, 27, 22, 18, 24, 130]
    }

    winning_hands = {
                     'singles': [227, 14, 6], 'pairs': [708, 49, 13], 
                     'two_pairs': [252, 11, 5], 'three_of_set': [142, 4, 2], 
                     'full_house': [21, 1, 0], 'poker': [11, 1, 0], 'flush': [0, 0, 0]
                     }
    total_winning_hands = sum(values[0] for values in winning_hands.values())
    total_winning_hands_6 = sum(values[1] for values in winning_hands.values())
    total_winning_hands_recent = sum(values[2] for values in winning_hands.values())

    pair_count = {
                  1: [81, 4, 0], 10: [92, 8, 1], 20: [120, 5, 2], 30: [107, 3, 1], 
                  40: [89, 8, 3], 50: [103, 11, 2], 60: [115, 10, 4]
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
              'all-time': [671, 690, 1361],
              'six-months': [38, 42, 80], 
              'recent-trends': [13, 13, 26]
            }

    sets = {
            'all-time' : [480, 491, 390, 1361],
            'six-months' : [26, 28, 26, 80],
            'recent-trends' : [6, 14, 6, 26]
           }

    return render_template('winning_hands_red.html', 
                           splits=splits,
                           sets=sets
                           )

@powerball.route('/trends', methods=['POST', 'GET'])
def trends():
    white_numbers_6 = [
                       2, 4, 7, 7, 8, 7, 5, 5, 3, 4, 
                       7, 3, 3, 5, 2, 7, 5, 11, 6, 4, 
                       9, 3, 4, 8, 5, 1, 8, 10, 4, 7, 
                       9, 4, 5, 5, 6, 9, 6, 5, 3, 5, 
                       6, 9, 6, 2, 2, 4, 8, 6, 5, 3, 
                       7, 13, 5, 4, 6, 11, 8, 8, 7, 8, 
                       4, 4, 10, 13, 7, 4, 2, 4, 3
                    ]

    white_numbers_trends = [
                        1, 1, 2, 3, 1, 0, 0, 1, 1, 1, 
                        0, 1, 2, 2, 1, 3, 2, 2, 1, 0, 
                        2, 1, 0, 4, 2, 0, 3, 1, 1, 4, 
                        4, 3, 1, 2, 2, 4, 3, 3, 1, 1, 
                        2, 3, 3, 2, 1, 3, 3, 2, 2, 0, 
                        3, 4, 0, 0, 2, 3, 3, 1, 2, 3, 
                        2, 1, 3, 6, 4, 2, 2, 1, 0
                    ]

    red_numbers_6 = [
                     6, 4, 3, 2, 4, 5, 2, 0, 0, 2, 
                     2, 5, 3, 6, 4, 1, 2, 2, 1, 5, 
                     3, 2, 5, 4, 2, 5
                    ]

    red_numbers_trends = [
                          1, 1, 2, 0, 1, 0, 1, 0, 0, 1, 
                          1, 3, 2, 3, 3, 0, 0, 1, 0, 1, 
                          0, 1, 0, 0, 1, 3
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
                     7.02, 7.45, 8.05, 7.07, 6.68, 7.03, 6.96, 6.53, 6.29, 6.42, 
                     6.96, 7.43, 5.13, 7.21, 6.61, 8.05, 7.11, 7.98, 7.85, 7.08, 
                     8.66, 6.69, 8.30, 7.49, 5.93, 5.23, 8.28, 9.43, 6.40, 7.38, 
                     7.01, 8.66, 8.45, 6.10, 5.99, 8.98, 8.06, 7.00, 7.58, 7.57, 
                     6.54, 6.81, 7.50, 7.51, 7.68, 5.77, 8.00, 6.06, 6.15, 6.86, 
                     6.46, 7.63, 7.67, 7.02, 6.29, 7.29, 7.26, 6.85, 7.83, 6.78, 
                     8.44, 8.14, 8.22, 8.80, 6.77, 7.41, 7.01, 7.05, 8.10
                     ]
    red_numbers = [
                   4.34, 3.89, 3.80, 4.82, 4.00, 3.48, 3.62, 3.27, 4.08, 3.46, 
                   3.36, 3.42, 3.71, 4.73, 3.25, 2.88, 3.16, 4.58, 3.55, 4.36, 
                   4.49, 3.48, 3.61, 4.43, 3.96, 4.27
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
                     [26, 33, 34, 57, 63],
                     [1, 18, 19, 39, 55],
                     [2, 7, 19, 31, 62],
                     [3, 31, 36, 44, 50],
                     [14, 40, 42, 51, 59]
                     ]
    red_numbers = [10, 17, 20, 22, 24]
    return render_template('predictions.html',
                            draw=draw, 
                            white_numbers=white_numbers, 
                            red_numbers=red_numbers
                            )