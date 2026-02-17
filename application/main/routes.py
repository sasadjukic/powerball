

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
              'all-time': [3217, 3256, 6560],
              'six-months': [204, 193, 400],
              'recent-trends': [68, 60, 130]
            }

    sets = {
            'all-time' : [834, 911, 981, 980, 902, 935, 1017, 6560],
            'six-months' : [50, 57, 66, 49, 49, 61, 68, 400],
            'recent-trends' : [19, 16, 25, 17, 14, 24, 15, 130]
    }

    winning_hands = {
                     'singles': [216, 13, 3], 'pairs': [682, 47, 18], 
                     'two_pairs': [245, 13, 4], 'three_of_set': [138, 4, 0], 
                     'full_house': [21, 3, 1], 'poker': [10, 0, 0], 'flush': [0, 0, 0]
                     }
    total_winning_hands = sum(values[0] for values in winning_hands.values())
    total_winning_hands_6 = sum(values[1] for values in winning_hands.values())
    total_winning_hands_recent = sum(values[2] for values in winning_hands.values())

    pair_count = {
                  1: [80, 4, 3], 10: [86, 5, 1], 20: [117, 6, 2], 30: [106, 4, 2], 
                  40: [83, 8, 2], 50: [99, 11, 5], 60: [110, 9, 4]
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
              'all-time': [645, 667, 1312],
              'six-months': [33, 47, 80], 
              'recent-trends': [11, 15, 26]
            }

    sets = {
            'all-time' : [464, 474, 374, 1312],
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
                       3, 5, 10, 4, 7, 5, 5, 9, 2, 5, 
                       6, 3, 4, 6, 6, 8, 3, 9, 7, 4, 
                       5, 6, 5, 5, 4, 6, 8, 15, 8, 4, 
                       7, 9, 5, 6, 3, 3, 5, 2, 5, 8, 
                       3, 4, 6, 5, 3, 4, 5, 5, 6, 3, 
                       10, 5, 11, 4, 3, 4, 5, 9, 7, 8, 
                       7, 7, 6, 9, 6, 8, 5, 6, 6
                    ]

    white_numbers_trends = [
                        0, 2, 2, 3, 6, 3, 0, 3, 0, 0, 
                        3, 0, 0, 1, 1, 2, 0, 5, 4, 2, 
                        5, 1, 1, 3, 2, 1, 4, 5, 1, 1, 
                        3, 0, 1, 3, 2, 2, 2, 1, 2, 4, 
                        1, 1, 2, 0, 1, 1, 0, 3, 1, 0, 
                        4, 2, 3, 1, 2, 3, 2, 5, 2, 4, 
                        1, 1, 4, 2, 1, 0, 0, 1, 1
                    ]

    red_numbers_6 = [
                     6, 4, 2, 4, 5, 2, 2, 0, 1, 2, 
                     2, 3, 0, 6, 4, 2, 4, 3, 5, 3, 
                     2, 4, 8, 2, 1, 3
                    ]

    red_numbers_trends = [
                          1, 1, 0, 2, 2, 2, 1, 0, 0, 0, 
                          1, 1, 0, 3, 1, 0, 1, 1, 1, 1, 
                          1, 0, 3, 2, 0, 1
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
                     7.30, 7.23, 7.67, 6.78, 6.75, 7.37, 6.69, 6.55, 6.26, 6.54, 
                     6.90, 7.64, 5.72, 6.43, 7.25, 7.36, 6.99, 7.73, 7.61, 6.89, 
                     9.08, 6.65, 8.62, 6.94, 6.49, 5.38, 8.64, 8.78, 6.47, 6.95, 
                     6.86, 8.32, 8.52, 6.13, 6.47, 8.09, 7.94, 7.16, 7.69, 7.41, 
                     6.42, 6.76, 7.23, 7.95, 7.40, 5.91, 7.92, 6.57, 6.11, 6.77, 
                     6.25, 7.32, 8.24, 7.17, 6.57, 7.07, 6.85, 7.08, 7.77, 6.71, 
                     8.96, 8.58, 8.16, 8.76, 6.73, 7.17, 7.59, 7.69, 8.04
                     ]
    red_numbers = [
                   4.57, 3.65, 3.89, 5.12, 4.43, 3.48, 3.46, 3.50, 4.16, 3.60, 
                   3.69, 3.07, 3.51, 4.51, 3.20, 2.75, 3.06, 3.86, 3.62, 4.26, 
                   4.97, 3.25, 3.60, 4.72, 4.21, 3.86
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
                     [31, 35, 39, 42, 51],
                     [7, 22, 28, 47, 48],
                     [6, 27, 30, 43, 59],
                     [1, 2, 58, 60, 66],
                     [13, 36, 37, 38, 44]
                     ]
    red_numbers = [6, 12, 17, 19, 23]
    return render_template('predictions.html',
                            draw=draw, 
                            white_numbers=white_numbers, 
                            red_numbers=red_numbers
                            )