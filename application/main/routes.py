

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

        # if user number is greater or equall to 70, then flash error
        if number >= 70:
            flash('Invalid Input')
            return redirect(url_for('search'))

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
              'all-time': [2946, 3006, 6030],
              'six-months': [197, 196, 400],
              'recent-trends': [64, 63, 130]
            }

    sets = {
            'all-time' : [762, 837, 896, 912, 836, 857, 930, 6030],
            'six-months' : [52, 57, 58, 59, 63, 63, 48, 400],
            'recent-trends' : [17, 18, 19, 20, 24, 17, 15, 130]
    }

    winning_hands = {
                     'singles': [195, 11, 2], 'pairs': [624, 44, 15], 
                     'two_pairs': [228, 14, 4], 'three_of_set': [131, 9, 3], 
                     'full_house': [18, 2, 2], 'poker': [10, 0, 0], 'flush': [0, 0, 0]
                     }
    total_winning_hands = sum(values[0] for values in winning_hands.values())
    total_winning_hands_6 = sum(values[1] for values in winning_hands.values())
    total_winning_hands_recent = sum(values[2] for values in winning_hands.values())

    pair_count = {
                  1: [76, 4, 1], 10: [81, 11, 3], 20: [110, 8, 4], 30: [101, 6, 2], 
                  40: [71, 7, 3], 50: [86, 3, 1], 60: [99, 5, 1]
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
              'all-time': [600, 606, 1206],
              'six-months': [41, 39, 80], 
              'recent-trends': [11, 15, 26]
            }

    sets = {
            'all-time' : [428, 438, 340, 1206],
            'six-months' : [31, 25, 24, 80],
            'recent-trends' : [7, 7, 12, 26]
           }

    return render_template('winning_hands_red.html', 
                           splits=splits,
                           sets=sets
                           )

@powerball.route('/trends', methods=['POST', 'GET'])
def trends():
    white_numbers_6 = [
                       6, 5, 4, 8, 5, 10, 6, 4, 4, 3, 
                       5, 9, 5, 4, 7, 7, 8, 7, 2, 7, 
                       6, 3, 13, 3, 3, 3, 4, 8, 8, 7, 
                       5, 6, 7, 5, 7, 6, 7, 4, 5, 8, 
                       4, 4, 8, 9, 6, 4, 7, 5, 8, 6, 
                       4, 10, 8, 7, 5, 5, 7, 4, 7, 8, 
                       4, 6, 4, 5, 4, 7, 4, 2, 4
                    ]

    white_numbers_trends = [
                        4, 1, 1, 3, 2, 1, 3, 0, 2, 2, 
                        0, 2, 3, 3, 3, 2, 1, 2, 0, 2, 
                        1, 0, 4, 2, 2, 1, 1, 2, 4, 2, 
                        2, 1, 2, 3, 3, 1, 4, 0, 2, 4, 
                        1, 3, 5, 2, 3, 1, 1, 3, 1, 1, 
                        2, 3, 2, 0, 0, 2, 2, 1, 4, 3, 
                        1, 1, 2, 1, 1, 2, 1, 1, 2
                    ]

    red_numbers_6 = [
                     7, 4, 3, 3, 3, 3, 2, 1, 5, 1, 
                     2, 4, 3, 4, 3, 0, 2, 3, 3, 8, 
                     2, 0, 1, 5, 7, 1
                    ]

    red_numbers_trends = [
                          1, 2, 1, 1, 1, 0, 0, 0, 1, 0, 
                          2, 0, 2, 0, 1, 0, 0, 0, 2, 2, 
                          2, 0, 0, 3, 5, 0
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
                     7.11, 7.39, 7.39, 6.65, 6.26, 7.69, 6.74, 6.19, 7.20, 6.89, 
                     7.10, 7.95, 5.45, 6.52, 7.25, 6.86, 7.17, 6.97, 7.67, 7.66, 
                     9.18, 7.32, 8.29, 7.21, 6.72, 5.63, 8.24, 7.54, 6.33, 7.23, 
                     6.84, 8.33, 8.78, 5.93, 6.34, 8.50, 8.34, 6.60, 8.24, 7.23, 
                     7.02, 6.60, 6.97, 7.95, 7.49, 6.10, 7.98, 6.19, 6.06, 7.22, 
                     5.95, 7.33, 7.76, 6.93, 6.84, 7.10, 7.25, 6.43, 7.81, 6.98, 
                     8.42, 8.46, 8.57, 8.43, 6.21, 7.31, 7.26, 7.55, 8.90
                     ]
    red_numbers = [
                   3.99, 3.51, 3.86, 4.77, 4.38, 3.61, 3.46, 3.62, 4.36, 3.94, 
                   3.58, 3.28, 3.83, 4.59, 3.23, 3.22, 3.25, 4.21, 3.57, 4.14, 
                   4.32, 3.31, 3.22, 4.25, 4.93, 3.57
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
                     [7, 25, 26, 42, 56],
                     [27, 38, 54, 59, 67],
                     [15, 19, 33, 64, 66],
                     [18, 21, 23, 36, 55],
                     [26, 32, 47, 52, 53]
                     ]
    red_numbers = [4, 9, 10, 14, 16]
    return render_template('predictions.html',
                            draw=draw, 
                            white_numbers=white_numbers, 
                            red_numbers=red_numbers
                            )