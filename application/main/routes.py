

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
              'all-time': [3221, 3262, 6570],
              'six-months': [206, 191, 400],
              'recent-trends': [67, 61, 130]
            }

    sets = {
            'all-time' : [835, 911, 983, 982, 904, 936, 1019, 6570],
            'six-months' : [51, 56, 67, 51, 48, 62, 65, 400],
            'recent-trends' : [17, 15, 26, 18, 15, 23, 16, 130]
    }

    winning_hands = {
                     'singles': [216, 13, 2], 'pairs': [683, 48, 18], 
                     'two_pairs': [246, 13, 5], 'three_of_set': [138, 3, 0], 
                     'full_house': [21, 3, 1], 'poker': [10, 0, 0], 'flush': [0, 0, 0]
                     }
    total_winning_hands = sum(values[0] for values in winning_hands.values())
    total_winning_hands_6 = sum(values[1] for values in winning_hands.values())
    total_winning_hands_recent = sum(values[2] for values in winning_hands.values())

    pair_count = {
                  1: [80, 4, 2], 10: [86, 5, 1], 20: [117, 6, 2], 30: [106, 4, 2], 
                  40: [83, 8, 2], 50: [99, 11, 5], 60: [111, 10, 4]
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
              'all-time': [646, 668, 1314],
              'six-months': [33, 47, 80], 
              'recent-trends': [11, 15, 26]
            }

    sets = {
            'all-time' : [465, 474, 375, 1314],
            'six-months' : [26, 31, 23, 80],
            'recent-trends' : [9, 9, 8, 26]
           }

    return render_template('winning_hands_red.html', 
                           splits=splits,
                           sets=sets
                           )

@powerball.route('/trends', methods=['POST', 'GET'])
def trends():
    white_numbers_6 = [
                       3, 5, 10, 4, 7, 5, 5, 9, 3, 5, 
                       6, 3, 4, 6, 5, 8, 3, 9, 7, 4, 
                       5, 6, 4, 5, 4, 6, 9, 16, 8, 4, 
                       7, 9, 6, 6, 3, 4, 5, 2, 5, 7, 
                       3, 4, 6, 5, 3, 3, 5, 6, 6, 3, 
                       10, 6, 11, 4, 3, 4, 5, 9, 7, 8, 
                       6, 7, 5, 9, 5, 9, 5, 6, 5
                    ]

    white_numbers_trends = [
                        0, 2, 1, 2, 5, 3, 0, 3, 1, 0, 
                        3, 0, 0, 1, 1, 2, 0, 4, 4, 2, 
                        5, 1, 1, 3, 2, 1, 5, 5, 1, 1, 
                        3, 0, 2, 3, 2, 2, 2, 1, 2, 4, 
                        0, 1, 2, 0, 1, 1, 0, 4, 2, 0, 
                        4, 2, 3, 0, 2, 3, 2, 5, 2, 4, 
                        1, 1, 4, 3, 1, 1, 0, 1, 0
                    ]

    red_numbers_6 = [
                     6, 4, 2, 4, 5, 2, 2, 0, 1, 2, 
                     2, 3, 0, 6, 4, 2, 4, 3, 5, 3, 
                     3, 4, 7, 2, 1, 3
                    ]

    red_numbers_trends = [
                          2, 1, 0, 2, 2, 2, 0, 0, 0, 0, 
                          1, 1, 0, 3, 1, 0, 1, 1, 1, 0, 
                          2, 0, 3, 2, 0, 1
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
                     6.80, 7.29, 7.36, 7.02, 6.45, 7.51, 6.73, 6.74, 7.24, 6.53, 
                     7.21, 7.66, 5.49, 6.27, 7.41, 7.18, 6.97, 6.82, 7.33, 7.30, 
                     8.70, 7.09, 8.73, 6.50, 6.45, 5.57, 8.42, 9.18, 6.70, 7.18, 
                     7.25, 8.71, 8.26, 5.98, 6.47, 8.15, 7.96, 6.54, 7.65, 7.45, 
                     6.67, 7.05, 6.87, 7.76, 8.03, 5.99, 7.63, 6.55, 6.23, 7.22, 
                     6.23, 7.66, 8.22, 6.91, 6.06, 7.34, 6.66, 7.22, 7.64, 7.01, 
                     8.67, 8.56, 8.82, 7.92, 6.50, 7.16, 7.39, 7.26, 8.52
                     ]
    red_numbers = [
                   4.03, 4.11, 3.69, 4.74, 4.27, 4.09, 3.18, 3.51, 4.22, 3.46, 
                   3.22, 3.53, 3.47, 4.29, 3.63, 3.08, 3.29, 4.03, 3.68, 3.91, 
                   5.03, 3.32, 3.78, 4.71, 4.05, 3.68
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
                     [21, 35, 45, 50, 52],
                     [25, 26, 33, 49, 51],
                     [2, 3, 6, 14, 31],
                     [13, 39, 41, 46, 62],
                     [9, 15, 29, 47, 68]
                     ]
    red_numbers = [7, 10, 12, 13, 25]
    return render_template('predictions.html',
                            draw=draw, 
                            white_numbers=white_numbers, 
                            red_numbers=red_numbers
                            )