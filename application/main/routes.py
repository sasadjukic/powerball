

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
              'all-time': [3025, 3081, 6190],
              'six-months': [196, 194, 400],
              'recent-trends': [65, 60, 130]
            }

    sets = {
            'all-time' : [785, 860, 917, 935, 858, 876, 959, 6190],
            'six-months' : [53, 56, 61, 54, 62, 55, 59, 400],
            'recent-trends' : [19, 20, 15, 20, 19, 14, 23, 130]
    }

    winning_hands = {
                     'singles': [204, 16, 6], 'pairs': [636, 40, 11], 
                     'two_pairs': [234, 13, 5], 'three_of_set': [136, 9, 4], 
                     'full_house': [18, 2, 0], 'poker': [10, 0, 0], 'flush': [0, 0, 0]
                     }
    total_winning_hands = sum(values[0] for values in winning_hands.values())
    total_winning_hands_6 = sum(values[1] for values in winning_hands.values())
    total_winning_hands_recent = sum(values[2] for values in winning_hands.values())

    pair_count = {
                  1: [76, 3, 0], 10: [82, 6, 1], 20: [111, 7, 1], 30: [102, 5, 1], 
                  40: [75, 10, 3], 50: [88, 3, 2], 60: [101, 5, 2]
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
              'all-time': [614, 624, 1238],
              'six-months': [39, 41, 80], 
              'recent-trends': [12, 14, 26]
            }

    sets = {
            'all-time' : [440, 444, 354, 1238],
            'six-months' : [29, 20, 31, 80],
            'recent-trends' : [12, 3, 11, 26]
           }

    return render_template('winning_hands_red.html', 
                           splits=splits,
                           sets=sets
                           )

@powerball.route('/trends', methods=['POST', 'GET'])
def trends():
    white_numbers_6 = [
                       5, 5, 3, 10, 6, 5, 8, 6, 5, 3, 
                       8, 7, 5, 5, 6, 8, 4, 6, 4, 6, 
                       6, 2, 14, 5, 6, 1, 3, 11, 7, 4, 
                       5, 2, 7, 8, 10, 6, 7, 2, 3, 9, 
                       4, 5, 9, 8, 6, 5, 4, 7, 5, 7, 
                       6, 10, 6, 3, 4, 3, 4, 4, 8, 6, 
                       7, 9, 7, 7, 6, 3, 4, 3, 7
                    ]

    white_numbers_trends = [
                        1, 1, 0, 3, 1, 2, 3, 5, 3, 0, 
                        3, 2, 1, 2, 3, 3, 0, 2, 4, 0, 
                        2, 1, 2, 2, 2, 0, 1, 5, 0, 0, 
                        3, 0, 4, 4, 5, 2, 1, 1, 0, 3, 
                        1, 1, 3, 2, 2, 2, 1, 2, 2, 3, 
                        2, 1, 1, 2, 1, 0, 1, 2, 1, 1, 
                        4, 3, 3, 3, 3, 0, 1, 1, 4
                    ]

    red_numbers_6 = [
                     5, 7, 2, 3, 4, 3, 0, 2, 3, 1, 
                     3, 3, 3, 2, 2, 0, 0, 2, 4, 7, 
                     4, 3, 2, 5, 10, 0
                    ]

    red_numbers_trends = [
                          1, 3, 1, 1, 2, 1, 0, 2, 1, 0, 
                          0, 0, 0, 1, 0, 0, 0, 2, 0, 1, 
                          2, 2, 2, 1, 3, 0
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
                     7.12, 7.10, 7.18, 7.20, 6.44, 7.85, 6.24, 6.88, 6.61, 6.31, 
                     7.43, 8.05, 5.37, 6.34, 6.94, 7.80, 7.19, 7.10, 7.36, 7.49, 
                     8.77, 6.67, 8.81, 7.25, 6.69, 5.54, 8.67, 7.87, 6.55, 7.03, 
                     7.03, 8.88, 8.81, 6.14, 6.15, 7.99, 8.38, 6.87, 8.01, 7.43, 
                     6.08, 6.98, 7.01, 8.10, 7.62, 6.05, 8.07, 6.79, 5.30, 7.33, 
                     6.14, 7.71, 7.43, 7.59, 6.53, 6.92, 6.71, 6.74, 7.82, 6.57, 
                     8.81, 7.93, 7.89, 9.02, 6.19, 7.38, 7.46, 7.32, 8.97
                     ]
    red_numbers = [
                   4.03, 3.79, 4.17, 4.72, 4.24, 3.62, 3.32, 3.68, 4.21, 3.35, 
                   3.47, 3.25, 3.96, 4.50, 3.17, 3.21, 3.04, 4.35, 3.63, 4.25, 
                   4.52, 3.26, 3.46, 4.52, 4.45, 3.83
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
                     [2, 15, 44, 48, 61],
                     [12, 18, 19, 55, 69],
                     [3, 10, 17, 47, 68],
                     [4, 25, 34, 42, 43],
                     [11, 32, 33, 62, 63]
                     ]
    red_numbers = [7, 9, 11, 15, 22]
    return render_template('predictions.html',
                            draw=draw, 
                            white_numbers=white_numbers, 
                            red_numbers=red_numbers
                            )