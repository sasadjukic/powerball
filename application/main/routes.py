

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
              'all-time': [3267, 3310, 6665],
              'six-months': [203, 193, 400],
              'recent-trends': [62, 67, 130]
            }

    sets = {
            'all-time' : [849, 929, 994, 990, 916, 957, 1030, 6665],
            'six-months' : [55, 59, 62, 49, 47, 71, 57, 400],
            'recent-trends' : [17, 22, 18, 12, 19, 27, 15, 130]
    }

    winning_hands = {
                     'singles': [221, 16, 5], 'pairs': [693, 47, 15], 
                     'two_pairs': [247, 10, 2], 'three_of_set': [140, 3, 2], 
                     'full_house': [21, 3, 1], 'poker': [11, 1, 1], 'flush': [0, 0, 0]
                     }
    total_winning_hands = sum(values[0] for values in winning_hands.values())
    total_winning_hands_6 = sum(values[1] for values in winning_hands.values())
    total_winning_hands_recent = sum(values[2] for values in winning_hands.values())

    pair_count = {
                  1: [81, 5, 1], 10: [90, 8, 4], 20: [118, 3, 2], 30: [106, 4, 0], 
                  40: [85, 8, 3], 50: [101, 11, 3], 60: [111, 8, 2]
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
              'all-time': [656, 677, 1333],
              'six-months': [36, 44, 80], 
              'recent-trends': [14, 12, 26]
            }

    sets = {
            'all-time' : [472, 477, 384, 1333],
            'six-months' : [26, 26, 28, 80],
            'recent-trends' : [11, 3, 12, 26]
           }

    return render_template('winning_hands_red.html', 
                           splits=splits,
                           sets=sets
                           )

@powerball.route('/trends', methods=['POST', 'GET'])
def trends():
    white_numbers_6 = [
                       2, 5, 8, 5, 8, 8, 9, 7, 3, 6, 
                       8, 4, 5, 6, 2, 5, 4, 12, 7, 6, 
                       7, 4, 4, 5, 3, 5, 7, 15, 6, 5, 
                       6, 7, 5, 4, 4, 6, 4, 3, 5, 6, 
                       4, 5, 7, 4, 1, 2, 8, 6, 4, 4, 
                       9, 10, 6, 6, 4, 8, 7, 10, 7, 7, 
                       3, 5, 7, 8, 5, 7, 4, 6, 5
                    ]

    white_numbers_trends = [
                        0, 1, 2, 1, 1, 5, 5, 0, 2, 2, 
                        4, 2, 1, 2, 0, 1, 2, 5, 3, 3, 
                        2, 2, 3, 1, 1, 0, 1, 4, 1, 2, 
                        1, 0, 2, 0, 1, 4, 1, 1, 0, 1, 
                        3, 5, 2, 0, 0, 0, 4, 3, 1, 3, 
                        1, 5, 0, 3, 2, 5, 2, 4, 2, 1, 
                        1, 1, 2, 5, 2, 1, 0, 1, 1
                    ]

    red_numbers_6 = [
                     8, 5, 2, 2, 3, 4, 2, 0, 0, 3, 
                     2, 4, 1, 5, 3, 1, 2, 2, 3, 5, 
                     4, 2, 8, 4, 1, 4
                    ]

    red_numbers_trends = [
                          4, 1, 0, 0, 2, 4, 0, 0, 0, 1, 
                          0, 1, 1, 0, 0, 0, 0, 0, 0, 3, 
                          2, 0, 1, 4, 1, 1
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
                     6.88, 6.86, 8.06, 6.73, 7.12, 7.81, 6.88, 6.34, 6.56, 6.88, 
                     7.20, 7.71, 5.37, 6.06, 6.56, 7.43, 6.74, 7.22, 7.36, 7.12, 
                     9.36, 6.74, 8.39, 6.89, 6.50, 6.40, 8.07, 9.24, 6.64, 7.70, 
                     6.63, 8.00, 8.31, 6.05, 6.82, 8.49, 7.65, 6.47, 7.53, 7.36, 
                     6.01, 6.88, 7.11, 7.81, 7.39, 5.38, 7.78, 6.73, 5.93, 7.21, 
                     6.85, 7.91, 7.95, 7.18, 6.91, 7.31, 6.87, 7.01, 8.02, 6.39, 
                     9.03, 8.10, 9.09, 8.23, 6.50, 7.18, 7.53, 7.02, 8.56
                     ]
    red_numbers = [
                   4.23, 3.90, 3.75, 4.95, 4.12, 3.65, 3.55, 2.96, 4.14, 3.65, 
                   3.63, 2.96, 3.42, 4.87, 3.07, 2.70, 3.34, 4.61, 3.87, 4.15, 
                   4.63, 3.25, 3.61, 4.80, 4.21, 3.98
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
                     [11, 16, 43, 49, 51],
                     [8, 23, 29, 55, 66],
                     [9, 45, 50, 52, 53],
                     [12, 23, 36, 39, 65],
                     [13, 37, 39, 47, 68]
                     ]
    red_numbers = [6, 7, 11, 13, 23]
    return render_template('predictions.html',
                            draw=draw, 
                            white_numbers=white_numbers, 
                            red_numbers=red_numbers
                            )