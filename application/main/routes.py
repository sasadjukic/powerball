

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
              'all-time': [3408, 3486, 6985],
              'six-months': [181, 216, 400],
              'recent-trends': [60, 69, 130]
            }

    sets = {
            'all-time' : [889, 974, 1030, 1035, 966, 1010, 1081, 6985],
            'six-months' : [52, 62, 44, 52, 61, 69, 60, 400],
            'recent-trends' : [23, 17, 15, 14, 17, 23, 21, 130]
    }

    winning_hands = {
                     'singles': [235, 18, 5], 'pairs': [725, 41, 14], 
                     'two_pairs': [259, 13, 4], 'three_of_set': [146, 8, 3], 
                     'full_house': [21, 0, 0], 'poker': [11, 0, 0], 'flush': [0, 0, 0]
                     }
    total_winning_hands = sum(values[0] for values in winning_hands.values())
    total_winning_hands_6 = sum(values[1] for values in winning_hands.values())
    total_winning_hands_recent = sum(values[2] for values in winning_hands.values())

    pair_count = {
                  1: [85, 5, 3], 10: [94, 8, 2], 20: [120, 2, 0], 30: [108, 2, 1], 
                  40: [92, 9, 2], 50: [108, 9, 4], 60: [117, 6, 2]
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
              'all-time': [693, 704, 1397],
              'six-months': [45, 35, 80], 
              'recent-trends': [16, 10, 26]
            }

    sets = {
            'all-time' : [496, 505, 396, 1397],
            'six-months' : [30, 30, 20, 80],
            'recent-trends' : [13, 9, 4, 26]
           }

    return render_template('winning_hands_red.html', 
                           splits=splits,
                           sets=sets
                           )

@powerball.route('/trends', methods=['POST', 'GET'])
def trends():
    white_numbers_6 = [
                       1, 5, 11, 7, 5, 7, 6, 5, 5, 7, 
                       4, 5, 6, 9, 2, 8, 10, 8, 3, 3, 
                       7, 3, 1, 6, 6, 4, 5, 4, 5, 9, 
                       6, 4, 2, 2, 3, 9, 7, 8, 2, 3, 
                       7, 9, 5, 7, 4, 5, 8, 7, 6, 9, 
                       3, 8, 5, 5, 7, 8, 8, 7, 9, 6, 
                       6, 4, 8, 11, 9, 4, 5, 4, 3
                    ]

    white_numbers_trends = [
                        0, 2, 3, 3, 4, 3, 1, 4, 3, 3, 
                        1, 2, 1, 3, 1, 1, 3, 2, 0, 1, 
                        1, 1, 0, 1, 3, 2, 2, 0, 4, 2, 
                        1, 1, 1, 0, 1, 3, 3, 2, 0, 2, 
                        1, 1, 1, 3, 2, 1, 1, 3, 2, 4, 
                        0, 0, 1, 4, 2, 2, 2, 5, 3, 1, 
                        2, 1, 3, 3, 4, 2, 3, 1, 1
                    ]

    red_numbers_6 = [
                     5, 6, 6, 2, 4, 3, 2, 1, 1, 3, 
                     2, 5, 5, 5, 4, 1, 2, 3, 0, 5, 
                     1, 2, 2, 2, 4, 4
                    ]

    red_numbers_trends = [
                          1, 3, 2, 2, 2, 0, 1, 1, 1, 2, 
                          0, 0, 1, 1, 0, 1, 2, 2, 0, 0, 
                          0, 1, 1, 0, 2, 0
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
                     6.84, 6.98, 8.24, 6.74, 6.69, 7.69, 6.94, 7.04, 6.88, 6.84, 
                     7.04, 7.45, 5.62, 6.90, 6.52, 7.80, 7.42, 7.47, 7.66, 7.24, 
                     8.31, 6.44, 8.19, 7.05, 6.21, 5.45, 7.84, 8.47, 6.63, 7.62, 
                     6.83, 8.28, 8.27, 6.11, 6.73, 8.57, 8.15, 6.79, 7.36, 7.21, 
                     6.15, 7.20, 7.11, 7.89, 7.24, 6.10, 7.75, 6.57, 6.58, 7.13, 
                     6.43, 8.02, 7.78, 7.14, 6.73, 6.92, 7.05, 6.51, 8.09, 6.90, 
                     8.60, 7.74, 8.52, 8.86, 6.37, 6.85, 7.49, 7.29, 8.48
                     ]
    red_numbers = [
                   4.65, 4.01, 4.09, 4.73, 4.34, 3.70, 3.20, 3.12, 4.13, 3.68, 
                   3.33, 3.72, 3.69, 4.32, 3.08, 2.72, 3.40, 4.49, 3.55, 3.96, 
                   5.07, 3.08, 3.47, 4.38, 4.22, 3.87
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
                     [12, 23, 28, 39, 50],
                     [38, 54, 55, 62, 67],
                     [2, 4, 5, 27, 69],
                     [11, 33, 38, 43, 54],
                     [23, 35, 46, 49, 63]
                     ]
    red_numbers = [3, 9, 16, 21, 25]
    return render_template('predictions.html',
                            draw=draw, 
                            white_numbers=white_numbers, 
                            red_numbers=red_numbers
                            )