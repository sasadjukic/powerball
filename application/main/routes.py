

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
              'all-time': [2877, 2938, 5890],
              'six-months': [201, 193, 400],
              'recent-trends': [63, 66, 130]
            }

    sets = {
            'all-time' : [744, 818, 875, 891, 810, 838, 914, 5890],
            'six-months' : [52, 56, 61, 59, 57, 60, 55, 400],
            'recent-trends' : [17, 18, 24, 12, 21, 22, 16, 130]
    }

    winning_hands = {
                     'singles': [192, 12, 5], 'pairs': [608, 45, 15], 
                     'two_pairs': [224, 13, 5], 'three_of_set': [128, 9, 1], 
                     'full_house': [16, 1, 0], 'poker': [10, 0, 0], 'flush': [0, 0, 0]
                     }
    total_winning_hands = sum(values[0] for values in winning_hands.values())
    total_winning_hands_6 = sum(values[1] for values in winning_hands.values())
    total_winning_hands_recent = sum(values[2] for values in winning_hands.values())

    pair_count = {
                  1: [75, 3, 2], 10: [78, 11, 3], 20: [106, 10, 3], 30: [99, 5, 2], 
                  40: [67, 5, 2], 50: [85, 4, 1], 60: [98, 6, 2]
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
              'all-time': [588, 590, 1178], 
              'six-months': [41, 39, 80], 
              'recent-trends': [16, 10, 26]
            }

    sets = {
            'all-time' : [420, 430, 328, 1178],
            'six-months' : [30, 28, 22, 80],
            'recent-trends' : [11, 9, 6, 26]
           }

    return render_template('winning_hands_red.html', 
                           splits=splits,
                           sets=sets
                           )

@powerball.route('/trends', methods=['POST', 'GET'])
def trends():
    white_numbers_6 = [
                       6, 5, 4, 7, 5, 11, 5, 5, 4, 2, 
                       6, 10, 5, 3, 5, 6, 8, 8, 3, 6, 
                       8, 4, 10, 4, 5, 4, 6, 7, 7, 7, 
                       6, 8, 7, 4, 6, 5, 5, 5, 6, 7, 
                       5, 1, 7, 8, 7, 4, 6, 5, 7, 6, 
                       4, 8, 7, 7, 6, 4, 8, 7, 3, 8, 
                       6, 7, 5, 8, 3, 7, 7, 1, 3
                    ]

    white_numbers_trends = [
                        0, 3, 1, 4, 2, 3, 3, 1, 0, 1, 
                        5, 2, 1, 0, 0, 2, 3, 4, 0, 3, 
                        4, 1, 6, 1, 1, 0, 0, 5, 3, 1, 
                        0, 1, 1, 1, 1, 4, 1, 1, 1, 2, 
                        2, 0, 1, 3, 2, 2, 3, 2, 4, 3, 
                        1, 3, 2, 2, 3, 2, 2, 1, 3, 3, 
                        1, 2, 2, 2, 2, 1, 1, 1, 1
                    ]

    red_numbers_6 = [
                     5, 3, 2, 3, 3, 4, 2, 2, 6, 2, 
                     1, 5, 3, 5, 4, 2, 3, 3, 0, 7, 
                     1, 3, 1, 3, 5, 2
                    ]

    red_numbers_trends = [
                          2, 2, 1, 1, 1, 2, 0, 0, 2, 1, 
                          0, 3, 1, 1, 2, 0, 0, 1, 0, 4, 
                          0, 0, 0, 0, 2, 0
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
                     6.97, 7.20, 7.60, 6.58, 5.91, 7.40, 6.39, 7.08, 6.69, 6.65, 
                     7.52, 8.03, 5.14, 6.29, 6.82, 6.99, 7.60, 6.52, 7.72, 7.58, 
                     9.39, 7.00, 9.35, 6.93, 6.08, 5.66, 8.57, 7.96, 6.44, 7.30, 
                     6.91, 9.03, 8.18, 5.78, 6.72, 8.55, 7.64, 7.24, 8.11, 7.26, 
                     7.02, 6.84, 6.86, 7.42, 7.60, 5.92, 8.00, 6.06, 5.52, 7.27, 
                     6.32, 7.26, 8.10, 7.34, 7.01, 7.32, 7.14, 6.03, 7.75, 6.85, 
                     9.06, 8.95, 8.16, 8.22, 6.27, 7.12, 7.51, 7.47, 8.83
                     ]
    red_numbers = [
                   3.72, 3.42, 3.76, 4.94, 4.05, 3.85, 3.71, 3.47, 4.56, 3.45, 
                   3.35, 3.34, 3.64, 4.32, 2.81, 3.24, 3.16, 4.64, 3.56, 4.18, 
                   4.49, 3.74, 3.46, 4.59, 4.24, 4.31
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
                     [2, 7, 59, 64, 69],
                     [23, 29, 58, 63, 68],
                     [4, 34, 37, 55, 60],
                     [33, 47, 61, 66, 67],
                     [13, 19, 30, 35, 41]
                     ]
    red_numbers = [9, 14, 18, 21, 24]
    return render_template('predictions.html',
                            draw=draw, 
                            white_numbers=white_numbers, 
                            red_numbers=red_numbers
                            )