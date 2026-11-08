

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
              'all-time': [3484, 3549, 7125],
              'six-months': [194, 203, 400],
              'recent-trends': [72, 57, 130]
            }

    sets = {
            'all-time' : [909, 1000, 1050, 1052, 986, 1035, 1093, 7125],
            'six-months' : [55, 65, 49, 49, 59, 71, 52, 400],
            'recent-trends' : [20, 23, 19, 16, 18, 22, 12, 130]
    }

    winning_hands = {
                     'singles': [235, 11, 0], 'pairs': [739, 41, 13], 
                     'two_pairs': [268, 18, 8], 'three_of_set': [151, 10, 5], 
                     'full_house': [21, 0, 0], 'poker': [11, 0, 0], 'flush': [0, 0, 0]
                     }
    total_winning_hands = sum(values[0] for values in winning_hands.values())
    total_winning_hands_6 = sum(values[1] for values in winning_hands.values())
    total_winning_hands_recent = sum(values[2] for values in winning_hands.values())

    pair_count = {
                  1: [87, 6, 2], 10: [96, 5, 1], 20: [122, 2, 2], 30: [110, 4, 2], 
                  40: [94, 8, 2], 50: [111, 10, 3], 60: [118, 6, 1]
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
              'all-time': [706, 719, 1425],
              'six-months': [43, 37, 80], 
              'recent-trends': [11, 15, 26]
            }

    sets = {
            'all-time' : [505, 514, 406, 1425],
            'six-months' : [28, 32, 20, 80],
            'recent-trends' : [7, 9, 10, 26]
           }

    return render_template('winning_hands_red.html', 
                           splits=splits,
                           sets=sets
                           )

@powerball.route('/trends', methods=['POST', 'GET'])
def trends():
    white_numbers_6 = [
                       3, 7, 9, 10, 7, 5, 3, 6, 5, 5, 
                       3, 4, 7, 10, 7, 10, 8, 6, 5, 3, 
                       8, 3, 4, 5, 5, 6, 4, 4, 7, 7, 
                       5, 6, 3, 4, 3, 5, 7, 7, 2, 6, 
                       6, 7, 2, 10, 4, 5, 5, 8, 6, 10, 
                       4, 3, 6, 6, 9, 9, 8, 8, 8, 5, 
                       6, 2, 3, 9, 9, 5, 5, 4, 4
                    ]

    white_numbers_trends = [
                        2, 3, 2, 5, 2, 1, 2, 1, 2, 0, 
                        2, 1, 3, 3, 3, 3, 2, 3, 3, 1, 
                        4, 1, 4, 2, 1, 2, 0, 1, 3, 2, 
                        1, 3, 2, 2, 1, 2, 2, 1, 0, 2, 
                        2, 5, 0, 3, 1, 1, 1, 1, 2, 3, 
                        2, 1, 1, 2, 4, 3, 3, 2, 1, 1, 
                        2, 0, 0, 2, 2, 1, 1, 1, 2
                    ]

    red_numbers_6 = [
                     2, 4, 6, 2, 4, 1, 4, 1, 4, 4, 
                     2, 4, 5, 6, 3, 1, 2, 3, 2, 5, 
                     2, 3, 5, 1, 3, 1
                    ]

    red_numbers_trends = [
                          1, 0, 1, 0, 1, 0, 2, 0, 2, 1, 
                          1, 0, 2, 2, 1, 0, 0, 0, 2, 3, 
                          2, 1, 3, 1, 0, 0
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
                     7.09, 7.53, 7.95, 6.63, 6.98, 8.16, 6.47, 6.79, 6.44, 6.67, 
                     6.39, 7.85, 5.77, 6.80, 7.09, 7.97, 6.79, 7.63, 7.31, 7.30, 
                     8.91, 6.71, 8.85, 7.61, 6.73, 5.77, 8.72, 7.69, 6.87, 7.42, 
                     6.64, 7.88, 8.57, 5.91, 6.74, 8.24, 8.18, 6.73, 7.38, 7.53, 
                     6.48, 6.83, 6.68, 8.19, 7.15, 5.70, 7.73, 6.76, 5.66, 7.64, 
                     6.36, 7.46, 7.88, 7.06, 6.44, 7.41, 7.24, 6.75, 7.81, 6.49, 
                     9.00, 8.22, 7.64, 8.59, 7.11, 7.18, 6.90, 7.15, 7.80
                ]
    red_numbers = [
                   4.30, 4.01, 4.22, 4.43, 4.27, 3.92, 3.43, 3.12, 4.31, 3.59, 
                   3.55, 3.39, 3.82, 4.55, 3.46, 3.01, 3.10, 4.54, 3.50, 4.18, 
                   4.55, 3.03, 3.56, 4.46, 4.51, 3.19
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
                     [18, 34, 51, 57, 67],
                     [12, 27, 59, 60, 64],
                     [1, 11, 29, 45, 67],
                     [23, 27, 55, 60, 66],
                     [37, 49, 50, 52, 59]
                     ]
    red_numbers = [1, 13, 20, 21, 24]
    return render_template('predictions.html',
                            draw=draw, 
                            white_numbers=white_numbers, 
                            red_numbers=red_numbers
                            )