

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
              'all-time': [3327, 3398, 6815],
              'six-months': [184, 210, 400],
              'recent-trends': [53, 75, 130]
            }

    sets = {
            'all-time' : [862, 947, 1009, 1017, 942, 981, 1057, 6815],
            'six-months' : [48, 52, 56, 57, 54, 74, 59, 400],
            'recent-trends' : [11, 15, 13, 26, 20, 21, 24, 130]
    }

    winning_hands = {
                     'singles': [227, 14, 6], 'pairs': [709, 48, 13], 
                     'two_pairs': [253, 12, 5], 'three_of_set': [142, 4, 2], 
                     'full_house': [21, 1, 0], 'poker': [11, 1, 0], 'flush': [0, 0, 0]
                     }
    total_winning_hands = sum(values[0] for values in winning_hands.values())
    total_winning_hands_6 = sum(values[1] for values in winning_hands.values())
    total_winning_hands_recent = sum(values[2] for values in winning_hands.values())

    pair_count = {
                  1: [81, 4, 0], 10: [92, 7, 1], 20: [120, 5, 2], 30: [107, 3, 1], 
                  40: [89, 8, 3], 50: [104, 11, 3], 60: [115, 10, 3]
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
              'all-time': [672, 691, 1363],
              'six-months': [39, 41, 80], 
              'recent-trends': [14, 12, 26]
            }

    sets = {
            'all-time' : [481, 491, 391, 1363],
            'six-months' : [27, 28, 25, 80],
            'recent-trends' : [7, 13, 6, 26]
           }

    return render_template('winning_hands_red.html', 
                           splits=splits,
                           sets=sets
                           )

@powerball.route('/trends', methods=['POST', 'GET'])
def trends():
    white_numbers_6 = [
                       2, 4, 8, 7, 8, 7, 5, 4, 3, 3, 
                       7, 3, 4, 5, 2, 6, 5, 11, 6, 4, 
                       9, 3, 4, 8, 6, 1, 8, 10, 3, 7, 
                       9, 3, 4, 5, 6, 9, 6, 5, 3, 5, 
                       6, 9, 6, 3, 2, 4, 8, 6, 5, 4, 
                       7, 12, 6, 4, 7, 10, 9, 8, 7, 9, 
                       4, 5, 10, 12, 7, 4, 2, 4, 2
                    ]

    white_numbers_trends = [
                        1, 1, 3, 3, 1, 0, 0, 1, 1, 1, 
                        0, 1, 2, 2, 1, 3, 2, 2, 1, 0, 
                        1, 1, 0, 4, 3, 0, 2, 1, 1, 4, 
                        4, 3, 1, 2, 2, 4, 3, 2, 1, 1, 
                        2, 3, 1, 3, 0, 3, 3, 2, 2, 1, 
                        3, 4, 1, 0, 3, 3, 4, 1, 1, 4, 
                        2, 2, 2, 5, 4, 2, 2, 1, 0
                    ]

    red_numbers_6 = [
                     6, 5, 3, 2, 4, 5, 2, 0, 0, 2, 
                     2, 5, 3, 6, 4, 1, 2, 2, 1, 5, 
                     3, 1, 5, 4, 2, 5
                    ]

    red_numbers_trends = [
                          1, 2, 2, 0, 1, 0, 1, 0, 0, 1, 
                          1, 3, 2, 3, 2, 0, 0, 1, 0, 1, 
                          0, 1, 1, 0, 1, 2
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
                     6.40, 7.20, 7.31, 7.20, 6.76, 7.36, 7.25, 6.26, 6.62, 6.25, 
                     7.10, 7.16, 5.52, 6.46, 6.62, 7.97, 7.10, 6.83, 7.61, 7.09, 
                     9.15, 6.68, 8.40, 7.31, 6.65, 5.38, 8.98, 8.39, 6.49, 7.89, 
                     7.33, 8.83, 8.24, 6.37, 6.34, 8.60, 7.97, 7.02, 7.59, 7.33, 
                     6.73, 7.20, 7.45, 7.44, 7.01, 6.02, 8.63, 6.56, 5.64, 6.89, 
                     6.43, 8.08, 7.56, 7.14, 6.42, 7.40, 6.80, 6.98, 7.46, 6.57, 
                     9.07, 8.25, 8.43, 8.65, 6.45, 7.36, 7.13, 6.77, 8.47
                     ]
    red_numbers = [
                   4.14, 3.82, 4.30, 4.69, 4.18, 3.58, 3.38, 3.52, 4.08, 3.09, 
                   3.62, 3.21, 3.83, 4.55, 3.41, 2.96, 3.23, 4.31, 3.42, 4.20, 
                   4.72, 3.13, 3.77, 4.26, 4.54, 4.06
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
                     [20, 27, 31, 35, 40],
                     [9, 22, 30, 47, 69],
                     [21, 25, 33, 45, 51],
                     [48, 52, 53, 54, 61],
                     [4, 23, 29, 30, 56]
                     ]
    red_numbers = [2, 7, 10, 11, 19]
    return render_template('predictions.html',
                            draw=draw, 
                            white_numbers=white_numbers, 
                            red_numbers=red_numbers
                            )