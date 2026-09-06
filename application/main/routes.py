

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
              'all-time': [3409, 3490, 6990],
              'six-months': [179, 218, 400],
              'recent-trends': [60, 69, 130]
            }

    sets = {
            'all-time' : [889, 975, 1030, 1035, 968, 1012, 1081, 6990],
            'six-months' : [51, 61, 44, 51, 63, 71, 59, 400],
            'recent-trends' : [23, 17, 15, 14, 18, 25, 18, 130]
    }

    winning_hands = {
                     'singles': [235, 18, 5], 'pairs': [725, 40, 14], 
                     'two_pairs': [260, 14, 5], 'three_of_set': [146, 8, 2], 
                     'full_house': [21, 0, 0], 'poker': [11, 0, 0], 'flush': [0, 0, 0]
                     }
    total_winning_hands = sum(values[0] for values in winning_hands.values())
    total_winning_hands_6 = sum(values[1] for values in winning_hands.values())
    total_winning_hands_recent = sum(values[2] for values in winning_hands.values())

    pair_count = {
                  1: [85, 5, 3], 10: [94, 7, 2], 20: [120, 2, 0], 30: [108, 2, 1], 
                  40: [92, 9, 2], 50: [108, 9, 4], 60: [117, 6, 2]
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
              'all-time': [694, 704, 1398],
              'six-months': [46, 34, 80], 
              'recent-trends': [16, 10, 26]
            }

    sets = {
            'all-time' : [497, 505, 396, 1398],
            'six-months' : [31, 30, 19, 80],
            'recent-trends' : [13, 9, 4, 26]
           }

    return render_template('winning_hands_red.html', 
                           splits=splits,
                           sets=sets
                           )

@powerball.route('/trends', methods=['POST', 'GET'])
def trends():
    white_numbers_6 = [
                       1, 4, 11, 7, 5, 7, 6, 5, 5, 7, 
                       4, 5, 6, 9, 3, 8, 9, 7, 3, 3, 
                       7, 3, 1, 6, 6, 4, 5, 4, 5, 9, 
                       6, 4, 2, 2, 3, 9, 7, 7, 2, 4, 
                       7, 9, 5, 7, 4, 5, 9, 7, 6, 9, 
                       3, 8, 6, 5, 7, 8, 8, 7, 10, 6, 
                       6, 3, 8, 11, 9, 4, 5, 4, 3
                    ]

    white_numbers_trends = [
                        0, 2, 3, 3, 4, 3, 1, 4, 3, 3, 
                        1, 2, 1, 3, 2, 1, 2, 2, 0, 1, 
                        1, 1, 0, 1, 3, 2, 2, 0, 4, 2, 
                        1, 1, 1, 0, 1, 3, 3, 2, 0, 3, 
                        1, 1, 1, 2, 2, 1, 2, 3, 2, 4, 
                        0, 0, 2, 4, 2, 2, 2, 5, 4, 1, 
                        2, 1, 2, 3, 4, 1, 2, 1, 1
                    ]

    red_numbers_6 = [
                     5, 6, 6, 2, 4, 3, 2, 1, 2, 3, 
                     2, 5, 5, 5, 4, 1, 2, 3, 0, 4, 
                     1, 2, 2, 2, 4, 4
                    ]

    red_numbers_trends = [
                          1, 3, 2, 1, 2, 0, 1, 1, 2, 2, 
                          0, 0, 1, 1, 0, 1, 2, 2, 0, 0, 
                          0, 1, 1, 0, 2, 0
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
                     6.84, 7.03, 8.06, 7.11, 6.70, 8.04, 6.85, 7.13, 6.58, 6.39, 
                     7.24, 7.47, 5.38, 7.01, 6.54, 7.67, 6.84, 7.57, 6.69, 7.27, 
                     9.05, 6.62, 8.54, 7.25, 7.00, 5.58, 8.75, 8.08, 6.72, 7.24, 
                     6.99, 8.00, 7.82, 5.81, 6.27, 7.53, 7.61, 6.91, 7.78, 7.45, 
                     6.64, 7.01, 7.48, 7.66, 7.39, 5.75, 7.92, 7.08, 6.03, 7.66, 
                     6.78, 7.69, 8.14, 6.64, 6.54, 7.16, 7.28, 7.14, 8.32, 6.46, 
                     9.25, 7.77, 8.41, 8.12, 6.79, 7.10, 7.01, 6.62, 8.75
                     ]
    red_numbers = [
                   4.12, 3.99, 3.83, 4.41, 4.34, 3.86, 3.27, 3.38, 4.17, 3.65, 
                   3.25, 3.50, 3.83, 4.52, 3.40, 2.77, 3.21, 3.87, 3.78, 4.43, 
                   4.76, 3.39, 3.89, 4.29, 4.39, 3.70
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
                     [30, 33, 36, 50, 52],
                     [14, 16, 28, 43, 61],
                     [14, 23, 30, 40, 69],
                     [22, 24, 43, 45, 69],
                     [8, 10, 18, 36, 55]
                     ]
    red_numbers = [1, 7, 12, 17, 19]
    return render_template('predictions.html',
                            draw=draw, 
                            white_numbers=white_numbers, 
                            red_numbers=red_numbers
                            )