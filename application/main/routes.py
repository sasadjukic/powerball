

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
              'all-time': [3271, 3321, 6680],
              'six-months': [200, 196, 400],
              'recent-trends': [58, 71, 130]
            }

    sets = {
            'all-time' : [851, 931, 994, 991, 920, 960, 1033, 6680],
            'six-months' : [54, 60, 60, 49, 48, 73, 56, 400],
            'recent-trends' : [17, 23, 14, 11, 19, 28, 18, 130]
    }

    winning_hands = {
                     'singles': [221, 16, 5], 'pairs': [696, 49, 15], 
                     'two_pairs': [247, 8, 2], 'three_of_set': [140, 3, 2], 
                     'full_house': [21, 3, 1], 'poker': [11, 1, 1], 'flush': [0, 0, 0]
                     }
    total_winning_hands = sum(values[0] for values in winning_hands.values())
    total_winning_hands_6 = sum(values[1] for values in winning_hands.values())
    total_winning_hands_recent = sum(values[2] for values in winning_hands.values())

    pair_count = {
                  1: [81, 5, 1], 10: [91, 9, 5], 20: [118, 3, 1], 30: [106, 4, 0], 
                  40: [86, 8, 3], 50: [101, 11, 2], 60: [112, 9, 3]
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
              'all-time': [658, 678, 1336],
              'six-months': [36, 44, 80], 
              'recent-trends': [14, 12, 26]
            }

    sets = {
            'all-time' : [474, 478, 384, 1336],
            'six-months' : [26, 26, 28, 80],
            'recent-trends' : [11, 4, 11, 26]
           }

    return render_template('winning_hands_red.html', 
                           splits=splits,
                           sets=sets
                           )

@powerball.route('/trends', methods=['POST', 'GET'])
def trends():
    white_numbers_6 = [
                       2, 5, 8, 5, 8, 9, 8, 6, 3, 5, 
                       8, 4, 5, 6, 2, 6, 5, 12, 7, 6, 
                       7, 4, 4, 5, 3, 5, 7, 14, 5, 5, 
                       6, 6, 5, 4, 4, 6, 4, 4, 5, 6, 
                       4, 6, 8, 3, 1, 2, 8, 5, 5, 4, 
                       9, 11, 7, 5, 4, 8, 7, 10, 8, 8, 
                       3, 5, 8, 9, 5, 6, 2, 5, 5
                    ]

    white_numbers_trends = [
                        0, 1, 3, 1, 1, 4, 5, 0, 2, 2, 
                        4, 2, 1, 2, 0, 2, 3, 5, 2, 2, 
                        2, 1, 3, 1, 0, 0, 1, 3, 1, 2, 
                        1, 0, 1, 0, 1, 3, 1, 2, 0, 0, 
                        3, 5, 3, 0, 0, 0, 5, 1, 2, 3, 
                        0, 6, 1, 3, 2, 5, 2, 3, 3, 2, 
                        1, 1, 3, 6, 2, 1, 0, 1, 1
                    ]

    red_numbers_6 = [
                     8, 4, 2, 2, 3, 5, 2, 0, 0, 3, 
                     2, 4, 1, 4, 4, 1, 2, 2, 3, 5, 
                     4, 2, 8, 4, 1, 4
                    ]

    red_numbers_trends = [
                          4, 1, 1, 0, 1, 4, 0, 0, 0, 1, 
                          0, 1, 1, 0, 1, 0, 0, 0, 0, 3, 
                          2, 0, 1, 3, 1, 1
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
                     6.54, 7.89, 7.51, 6.65, 6.52, 7.44, 6.75, 6.70, 6.50, 6.67, 
                     7.23, 7.74, 5.52, 6.12, 7.05, 7.59, 6.78, 7.15, 7.28, 7.40, 
                     8.64, 6.73, 8.49, 6.97, 6.26, 5.35, 8.24, 8.99, 6.62, 6.88, 
                     7.24, 8.15, 8.72, 6.35, 6.30, 8.34, 7.82, 6.98, 7.95, 7.62, 
                     6.57, 6.70, 7.62, 7.30, 7.58, 6.20, 7.89, 6.61, 6.04, 7.31, 
                     6.61, 8.05, 7.49, 7.13, 6.54, 7.06, 7.00, 7.06, 7.75, 6.89, 
                     8.65, 8.00, 8.17, 8.65, 6.20, 7.78, 7.82, 7.07, 8.59
                     ]
    red_numbers = [
                   4.27, 3.87, 3.73, 4.89, 4.53, 3.68, 3.46, 3.22, 4.24, 3.21, 
                   3.62, 3.37, 3.67, 4.77, 3.37, 2.67, 3.32, 4.16, 3.76, 4.54, 
                   4.53, 3.27, 3.74, 4.55, 4.12, 3.44
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
                     [27, 28, 38, 66, 67],
                     [10, 20, 34, 42, 63],
                     [11, 14, 39, 57, 58],
                     [16, 21, 47, 55, 61],
                     [16, 35, 36, 56, 67]
                     ]
    red_numbers = [6, 12, 15, 21, 23]
    return render_template('predictions.html',
                            draw=draw, 
                            white_numbers=white_numbers, 
                            red_numbers=red_numbers
                            )