

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
              'all-time': [3052, 3109, 6245],
              'six-months': [196, 194, 400],
              'recent-trends': [62, 65, 130]
            }

    sets = {
            'all-time' : [791, 866, 929, 939, 867, 884, 969, 6245],
            'six-months' : [55, 51, 63, 53, 64, 52, 62, 400],
            'recent-trends' : [16, 19, 17, 18, 20, 14, 26, 130]
    }

    winning_hands = {
                     'singles': [205, 16, 4], 'pairs': [644, 42, 14], 
                     'two_pairs': [235, 11, 4], 'three_of_set': [137, 9, 4], 
                     'full_house': [18, 2, 0], 'poker': [10, 0, 0], 'flush': [0, 0, 0]
                     }
    total_winning_hands = sum(values[0] for values in winning_hands.values())
    total_winning_hands_6 = sum(values[1] for values in winning_hands.values())
    total_winning_hands_recent = sum(values[2] for values in winning_hands.values())

    pair_count = {
                  1: [76, 2, 0], 10: [82, 4, 1], 20: [114, 10, 4], 30: [102, 4, 1], 
                  40: [76, 10, 3], 50: [90, 5, 2], 60: [103, 6, 3]
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
              'all-time': [619, 630, 1249],
              'six-months': [39, 41, 80], 
              'recent-trends': [13, 13, 26]
            }

    sets = {
            'all-time' : [445, 448, 356, 1249],
            'six-months' : [30, 21, 29, 80],
            'recent-trends' : [13, 6, 7, 26]
           }

    return render_template('winning_hands_red.html', 
                           splits=splits,
                           sets=sets
                           )

@powerball.route('/trends', methods=['POST', 'GET'])
def trends():
    white_numbers_6 = [
                       5, 4, 6, 9, 6, 5, 9, 6, 5, 2, 
                       5, 6, 4, 6, 8, 8, 3, 5, 4, 5, 
                       5, 3, 13, 5, 7, 2, 4, 9, 10, 5, 
                       5, 3, 7, 7, 10, 4, 8, 1, 3, 8, 
                       5, 8, 9, 8, 7, 6, 3, 6, 4, 7, 
                       5, 9, 10, 3, 2, 2, 4, 3, 7, 4, 
                       9, 10, 5, 10, 5, 4, 5, 2, 8
                    ]

    white_numbers_trends = [
                        0, 1, 3, 2, 0, 2, 3, 3, 2, 0, 
                        3, 1, 0, 3, 5, 3, 0, 2, 2, 0, 
                        0, 2, 4, 2, 1, 1, 2, 2, 3, 1, 
                        3, 1, 2, 3, 3, 2, 2, 1, 0, 4, 
                        2, 3, 2, 2, 2, 2, 1, 0, 2, 4, 
                        1, 0, 5, 1, 0, 0, 1, 0, 2, 1, 
                        4, 5, 1, 6, 3, 1, 2, 1, 2
                    ]

    red_numbers_6 = [
                     5, 7, 2, 4, 5, 2, 0, 2, 3, 1, 
                     3, 3, 2, 1, 2, 0, 2, 2, 5, 5, 
                     4, 4, 2, 5, 9, 0
                    ]

    red_numbers_trends = [
                          2, 2, 1, 2, 3, 0, 0, 1, 2, 0, 
                          0, 0, 0, 1, 1, 0, 2, 1, 1, 1, 
                          1, 2, 2, 0, 1, 0
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
                     7.30, 7.10, 7.80, 7.06, 6.68, 7.59, 6.95, 6.77, 6.61, 6.60, 
                     6.91, 8.07, 5.16, 6.59, 7.24, 7.69, 6.80, 6.72, 7.04, 7.46, 
                     8.75, 7.05, 8.88, 7.05, 6.34, 5.39, 8.20, 7.69, 6.75, 7.17, 
                     6.85, 8.10, 8.60, 6.10, 6.50, 8.55, 7.97, 7.23, 7.87, 8.17, 
                     6.35, 6.52, 6.72, 8.28, 7.68, 6.16, 7.83, 6.52, 5.20, 7.50, 
                     6.27, 7.54, 8.01, 7.12, 6.91, 6.89, 6.70, 6.76, 8.22, 6.41, 
                     9.06, 8.29, 8.92, 8.70, 6.10, 6.63, 7.21, 7.10, 9.05
                     ]
    red_numbers = [
                   4.07, 3.63, 3.79, 4.93, 4.47, 3.97, 3.48, 3.44, 4.18, 3.26, 
                   3.46, 3.26, 3.99, 4.49, 2.94, 2.94, 3.43, 4.47, 3.62, 4.48, 
                   4.86, 3.15, 3.09, 4.66, 4.21, 3.73
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
                     [15, 24, 36, 60, 69],
                     [18, 29, 33, 37, 38],
                     [21, 26, 31, 53, 61],
                     [23, 25, 27, 46, 52],
                     [8, 10, 30, 49, 51]
                     ]
    red_numbers = [2, 4, 7, 25, 26]
    return render_template('predictions.html',
                            draw=draw, 
                            white_numbers=white_numbers, 
                            red_numbers=red_numbers
                            )