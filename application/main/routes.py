

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
              'all-time': [3086, 3130, 6300],
              'six-months': [204, 187, 400],
              'recent-trends': [71, 59, 130]
            }

    sets = {
            'all-time' : [798, 879, 938, 944, 874, 889, 978, 6300],
            'six-months' : [53, 60, 61, 52, 62, 49, 63, 400],
            'recent-trends' : [14, 24, 22, 13, 18, 15, 24, 130]
    }

    winning_hands = {
                     'singles': [206, 13, 3], 'pairs': [649, 40, 14], 
                     'two_pairs': [239, 15, 6], 'three_of_set': [137, 9, 2], 
                     'full_house': [19, 3, 1], 'poker': [10, 0, 0], 'flush': [0, 0, 0]
                     }
    total_winning_hands = sum(values[0] for values in winning_hands.values())
    total_winning_hands_6 = sum(values[1] for values in winning_hands.values())
    total_winning_hands_recent = sum(values[2] for values in winning_hands.values())

    pair_count = {
                  1: [76, 1, 0], 10: [84, 6, 3], 20: [115, 9, 4], 30: [102, 3, 0], 
                  40: [78, 10, 3], 50: [90, 5, 2], 60: [103, 5, 2]
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
              'all-time': [625, 635, 1260],
              'six-months': [36, 44, 80], 
              'recent-trends': [12, 14, 26]
            }

    sets = {
            'all-time' : [448, 456, 356, 1260],
            'six-months' : [27, 25, 28, 80],
            'recent-trends' : [9, 13, 4, 26]
           }

    return render_template('winning_hands_red.html', 
                           splits=splits,
                           sets=sets
                           )

@powerball.route('/trends', methods=['POST', 'GET'])
def trends():
    white_numbers_6 = [
                       6, 4, 8, 7, 4, 3, 8, 8, 5, 5, 
                       5, 5, 7, 7, 9, 9, 3, 6, 4, 3, 
                       4, 3, 10, 5, 6, 2, 7, 12, 9, 3, 
                       6, 6, 7, 8, 9, 3, 7, 1, 2, 9, 
                       3, 8, 9, 7, 7, 4, 4, 6, 5, 7, 
                       5, 8, 8, 4, 2, 2, 3, 4, 6, 5, 
                       9, 8, 5, 9, 6, 5, 6, 3, 7
                    ]

    white_numbers_trends = [
                        1, 1, 6, 0, 0, 0, 2, 3, 1, 3, 
                        3, 1, 3, 3, 3, 4, 1, 2, 1, 1, 
                        0, 3, 2, 1, 1, 1, 4, 5, 4, 1, 
                        2, 4, 1, 3, 0, 0, 2, 0, 0, 2, 
                        2, 3, 0, 2, 2, 1, 3, 1, 2, 2, 
                        1, 1, 5, 2, 1, 0, 0, 1, 2, 1, 
                        4, 3, 0, 5, 2, 3, 3, 2, 1
                    ]

    red_numbers_6 = [
                     3, 6, 3, 4, 5, 1, 0, 2, 3, 2, 
                     3, 2, 2, 3, 3, 1, 2, 2, 5, 5, 
                     4, 4, 2, 5, 8, 0
                    ]

    red_numbers_trends = [
                          1, 1, 1, 2, 3, 0, 0, 0, 1, 2, 
                          0, 1, 0, 2, 2, 1, 2, 1, 2, 1, 
                          0, 2, 0, 0, 1, 0
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
                     6.95, 6.97, 7.82, 6.86, 6.06, 8.00, 6.84, 6.37, 7.19, 6.93, 
                     7.24, 7.56, 5.57, 6.58, 7.09, 7.31, 7.38, 6.99, 7.69, 6.92, 
                     9.00, 6.61, 9.10, 6.69, 6.34, 5.35, 9.02, 8.12, 6.69, 7.30, 
                     6.97, 7.84, 8.70, 6.13, 6.33, 7.99, 8.29, 7.22, 7.92, 7.66, 
                     6.31, 6.74, 6.64, 7.69, 7.67, 5.56, 7.87, 5.99, 5.99, 7.39, 
                     6.41, 7.86, 8.16, 7.09, 6.77, 6.51, 6.83, 6.52, 7.83, 7.08, 
                     9.13, 7.85, 8.61, 8.32, 6.34, 6.80, 8.14, 7.26, 9.05
                     ]
    red_numbers = [
                   4.05, 3.86, 4.16, 4.83, 3.94, 3.53, 3.53, 3.46, 4.31, 3.79, 
                   3.45, 2.94, 3.56, 4.78, 2.97, 3.43, 3.52, 4.65, 3.46, 4.25, 
                   4.47, 3.53, 2.98, 4.74, 4.23, 3.58
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
                     [4, 15, 33, 37, 64],
                     [9, 17, 21, 24, 42],
                     [25, 26, 41, 44, 53],
                     [8, 19, 30, 61, 68],
                     [13, 18, 35, 45, 62]
                     ]
    red_numbers = [4, 5, 9, 20, 22]
    return render_template('predictions.html',
                            draw=draw, 
                            white_numbers=white_numbers, 
                            red_numbers=red_numbers
                            )