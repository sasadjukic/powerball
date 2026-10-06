

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
              'all-time': [3445, 3519, 7055],
              'six-months': [183, 214, 400],
              'recent-trends': [65, 64, 130]
            }

    sets = {
            'all-time' : [898, 986, 1042, 1041, 978, 1023, 1087, 7055],
            'six-months' : [52, 58, 49, 52, 64, 67, 58, 400],
            'recent-trends' : [18, 21, 19, 13, 15, 23, 21, 130]
    }

    winning_hands = {
                     'singles': [235, 15, 2], 'pairs': [733, 41, 15], 
                     'two_pairs': [262, 15, 4], 'three_of_set': [149, 9, 5], 
                     'full_house': [21, 0, 0], 'poker': [11, 0, 0], 'flush': [0, 0, 0]
                     }
    total_winning_hands = sum(values[0] for values in winning_hands.values())
    total_winning_hands_6 = sum(values[1] for values in winning_hands.values())
    total_winning_hands_recent = sum(values[2] for values in winning_hands.values())

    pair_count = {
                  1: [86, 6, 2], 10: [96, 6, 3], 20: [121, 3, 1], 30: [109, 3, 2], 
                  40: [94, 9, 2], 50: [108, 7, 3], 60: [118, 7, 2]
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
              'all-time': [701, 710, 1411],
              'six-months': [47, 33, 80], 
              'recent-trends': [15, 11, 26]
            }

    sets = {
            'all-time' : [502, 509, 400, 1411],
            'six-months' : [32, 32, 16, 80],
            'recent-trends' : [10, 10, 6, 26]
           }

    return render_template('winning_hands_red.html', 
                           splits=splits,
                           sets=sets
                           )

@powerball.route('/trends', methods=['POST', 'GET'])
def trends():
    white_numbers_6 = [
                       1, 6, 10, 8, 6, 7, 3, 5, 6, 5, 
                       1, 3, 6, 9, 5, 10, 10, 5, 4, 3, 
                       7, 2, 3, 7, 7, 5, 5, 3, 7, 9, 
                       5, 5, 3, 2, 3, 8, 7, 7, 3, 6, 
                       6, 9, 4, 9, 5, 5, 6, 7, 7, 7, 
                       3, 6, 6, 5, 8, 6, 9, 8, 9, 6, 
                       6, 3, 6, 10, 10, 4, 6, 4, 3
                    ]

    white_numbers_trends = [
                        0, 2, 2, 3, 3, 2, 1, 2, 3, 2, 
                        1, 1, 1, 2, 4, 3, 3, 2, 2, 1, 
                        3, 0, 3, 1, 3, 2, 1, 1, 4, 2, 
                        1, 2, 2, 0, 1, 1, 2, 1, 1, 3, 
                        1, 3, 0, 2, 2, 0, 1, 0, 3, 1, 
                        0, 1, 1, 4, 4, 2, 3, 5, 2, 0, 
                        2, 1, 2, 4, 4, 1, 3, 2, 2
                    ]

    red_numbers_6 = [
                     3, 5, 8, 2, 4, 2, 4, 1, 3, 4, 
                     2, 4, 5, 7, 4, 1, 2, 3, 0, 3, 
                     0, 3, 3, 1, 3, 3
                    ]

    red_numbers_trends = [
                          0, 2, 2, 0, 0, 0, 3, 0, 3, 3, 
                          0, 0, 2, 3, 0, 0, 1, 1, 0, 1, 
                          0, 2, 2, 1, 0, 0
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
                     6.85, 7.39, 8.36, 6.89, 7.32, 8.21, 6.67, 6.54, 7.31, 6.58, 
                     7.02, 7.64, 5.16, 6.87, 6.82, 7.61, 7.42, 7.55, 7.01, 7.00, 
                     8.87, 5.74, 8.67, 7.79, 6.22, 5.69, 7.72, 8.50, 6.58, 7.56, 
                     6.75, 8.40, 8.03, 5.75, 6.34, 8.27, 7.78, 6.56, 7.54, 7.66, 
                     6.38, 6.92, 6.74, 7.66, 7.37, 5.78, 8.06, 6.38, 5.71, 7.13, 
                     6.32, 7.81, 7.67, 7.19, 6.92, 7.01, 7.10, 6.92, 8.56, 6.86, 
                     9.18, 7.74, 8.44, 8.68, 6.78, 7.17, 7.78, 6.85, 8.25
                ]
    red_numbers = [
                   4.06, 4.10, 4.13, 4.69, 3.99, 3.77, 3.16, 3.07, 4.12, 3.86, 
                   3.12, 3.51, 3.69, 5.16, 3.64, 3.05, 3.20, 4.14, 3.46, 4.13, 
                   4.30, 3.14, 3.78, 4.64, 4.38, 3.71
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
                     [24, 43, 53, 60, 66],
                     [34, 36, 39, 49, 52],
                     [4, 15, 24, 35, 52],
                     [7, 17, 32, 51, 66],
                     [4, 20, 52, 66, 69]
                     ]
    red_numbers = [1, 7, 13, 18, 23]
    return render_template('predictions.html',
                            draw=draw, 
                            white_numbers=white_numbers, 
                            red_numbers=red_numbers
                            )