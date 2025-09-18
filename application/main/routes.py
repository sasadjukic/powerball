

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
              'all-time': [3048, 3103, 6235],
              'six-months': [198, 192, 400],
              'recent-trends': [66, 60, 130]
            }

    sets = {
            'all-time' : [790, 865, 927, 939, 865, 883, 966, 6235],
            'six-months' : [55, 53, 63, 54, 63, 52, 60, 400],
            'recent-trends' : [17, 21, 17, 20, 19, 13, 23, 130]
    }

    winning_hands = {
                     'singles': [205, 17, 5], 'pairs': [643, 42, 14], 
                     'two_pairs': [235, 11, 4], 'three_of_set': [136, 8, 3], 
                     'full_house': [18, 2, 0], 'poker': [10, 0, 0], 'flush': [0, 0, 0]
                     }
    total_winning_hands = sum(values[0] for values in winning_hands.values())
    total_winning_hands_6 = sum(values[1] for values in winning_hands.values())
    total_winning_hands_recent = sum(values[2] for values in winning_hands.values())

    pair_count = {
                  1: [76, 2, 0], 10: [82, 5, 1], 20: [114, 10, 4], 30: [102, 4, 1], 
                  40: [75, 9, 2], 50: [90, 5, 2], 60: [103, 6, 3]
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
              'all-time': [618, 629, 1247],
              'six-months': [39, 41, 80], 
              'recent-trends': [13, 13, 26]
            }

    sets = {
            'all-time' : [444, 447, 356, 1247],
            'six-months' : [30, 21, 29, 80],
            'recent-trends' : [13, 5, 8, 26]
           }

    return render_template('winning_hands_red.html', 
                           splits=splits,
                           sets=sets
                           )

@powerball.route('/trends', methods=['POST', 'GET'])
def trends():
    white_numbers_6 = [
                       5, 4, 5, 9, 6, 5, 9, 7, 5, 2, 
                       7, 6, 4, 6, 7, 8, 3, 6, 4, 5, 
                       6, 3, 14, 5, 7, 2, 4, 9, 8, 5, 
                       5, 3, 7, 7, 10, 4, 8, 2, 3, 8, 
                       5, 7, 9, 8, 7, 5, 3, 6, 5, 7, 
                       5, 9, 10, 3, 2, 2, 4, 3, 7, 5, 
                       9, 10, 5, 9, 5, 3, 4, 2, 8
                    ]

    white_numbers_trends = [
                        0, 2, 2, 2, 0, 2, 3, 4, 2, 0, 
                        4, 1, 0, 3, 4, 3, 0, 3, 3, 0, 
                        0, 2, 4, 2, 2, 1, 2, 3, 1, 1, 
                        3, 1, 3, 3, 4, 2, 2, 1, 0, 4, 
                        2, 3, 2, 2, 2, 1, 1, 0, 2, 4, 
                        1, 0, 5, 1, 0, 0, 1, 0, 1, 1, 
                        4, 5, 1, 5, 3, 0, 1, 1, 2
                    ]

    red_numbers_6 = [
                     5, 7, 2, 3, 5, 2, 0, 2, 4, 1, 
                     3, 3, 2, 1, 2, 0, 2, 2, 5, 5, 
                     4, 4, 2, 5, 9, 0
                    ]

    red_numbers_trends = [
                          2, 3, 1, 1, 3, 0, 0, 1, 2, 0, 
                          0, 0, 0, 1, 0, 0, 2, 1, 1, 1, 
                          1, 2, 2, 0, 2, 0
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
                     6.99, 7.41, 7.37, 7.25, 6.40, 7.50, 6.91, 6.48, 7.11, 6.47, 
                     7.06, 7.93, 4.98, 6.63, 6.98, 6.97, 6.48, 7.02, 7.84, 7.02, 
                     8.63, 6.63, 9.03, 7.39, 6.46, 5.53, 8.65, 8.22, 6.62, 7.09, 
                     6.80, 8.18, 8.59, 6.23, 6.61, 8.47, 8.85, 7.19, 8.40, 7.34, 
                     6.74, 6.42, 6.80, 8.13, 7.31, 5.93, 8.09, 5.98, 5.68, 7.24, 
                     6.28, 7.62, 8.07, 6.84, 6.36, 6.74, 7.38, 6.40, 7.55, 7.02, 
                     9.05, 8.62, 8.53, 8.66, 6.05, 7.36, 7.31, 7.68, 8.45
                     ]
    red_numbers = [
                   3.65, 3.31, 3.87, 4.80, 4.04, 3.68, 3.71, 3.49, 4.37, 3.72, 
                   3.65, 3.03, 3.79, 4.58, 3.20, 2.95, 3.38, 4.66, 3.35, 4.24, 
                   4.73, 3.30, 3.32, 4.94, 4.58, 3.66
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
                     [4, 10, 35, 54, 59],
                     [5, 17, 32, 47, 51],
                     [18, 19, 24, 55, 69],
                     [3, 16, 23, 37, 64],
                     [1, 25, 40, 63, 65]
                     ]
    red_numbers = [3, 9, 13, 14, 23]
    return render_template('predictions.html',
                            draw=draw, 
                            white_numbers=white_numbers, 
                            red_numbers=red_numbers
                            )