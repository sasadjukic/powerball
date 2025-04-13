

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
              'all-time': [2879, 2941, 5895],
              'six-months': [200, 194, 400],
              'recent-trends': [61, 68, 130]
            }

    sets = {
            'all-time' : [744, 819, 876, 891, 812, 839, 914, 5895],
            'six-months' : [52, 56, 62, 57, 59, 60, 54, 400],
            'recent-trends' : [16, 17, 24, 12, 22, 23, 16, 130]
    }

    winning_hands = {
                     'singles': [192, 12, 5], 'pairs': [609, 45, 15], 
                     'two_pairs': [224, 13, 5], 'three_of_set': [128, 9, 1], 
                     'full_house': [16, 1, 0], 'poker': [10, 0, 0], 'flush': [0, 0, 0]
                     }
    total_winning_hands = sum(values[0] for values in winning_hands.values())
    total_winning_hands_6 = sum(values[1] for values in winning_hands.values())
    total_winning_hands_recent = sum(values[2] for values in winning_hands.values())

    pair_count = {
                  1: [75, 3, 2], 10: [78, 11, 2], 20: [106, 10, 3], 30: [99, 5, 2], 
                  40: [68, 6, 3], 50: [85, 4, 1], 60: [98, 6, 2]
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
              'all-time': [588, 591, 1179], 
              'six-months': [41, 39, 80], 
              'recent-trends': [15, 11, 26]
            }

    sets = {
            'all-time' : [420, 431, 328, 1178],
            'six-months' : [30, 29, 21, 80],
            'recent-trends' : [10, 10, 6, 26]
           }

    return render_template('winning_hands_red.html', 
                           splits=splits,
                           sets=sets
                           )

@powerball.route('/trends', methods=['POST', 'GET'])
def trends():
    white_numbers_6 = [
                       6, 5, 4, 7, 5, 11, 5, 5, 4, 2, 
                       6, 10, 5, 3, 5, 7, 8, 7, 3, 6, 
                       8, 5, 10, 4, 5, 4, 6, 7, 7, 6, 
                       5, 8, 7, 4, 6, 5, 5, 5, 6, 7, 
                       5, 1, 7, 9, 8, 4, 6, 5, 7, 6, 
                       4, 7, 8, 7, 6, 4, 8, 7, 3, 8, 
                       6, 7, 4, 8, 3, 7, 7, 1, 3
                    ]

    white_numbers_trends = [
                        0, 2, 1, 4, 2, 3, 3, 1, 0, 1, 
                        5, 2, 1, 0, 0, 3, 2, 3, 0, 3, 
                        4, 2, 6, 1, 1, 0, 0, 5, 2, 1, 
                        0, 1, 1, 1, 1, 4, 1, 1, 1, 2, 
                        2, 0, 0, 4, 3, 2, 3, 2, 4, 3, 
                        1, 3, 3, 2, 3, 2, 2, 1, 3, 3, 
                        1, 2, 2, 2, 2, 1, 1, 1, 1
                    ]

    red_numbers_6 = [
                     5, 3, 2, 3, 3, 4, 2, 2, 6, 2, 
                     1, 5, 3, 5, 4, 2, 3, 3, 1, 7, 
                     1, 2, 1, 3, 5, 2
                    ]

    red_numbers_trends = [
                          2, 2, 0, 1, 1, 2, 0, 0, 2, 1, 
                          0, 3, 1, 1, 2, 0, 0, 1, 1, 4, 
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
                     6.69, 7.40, 7.61, 6.66, 6.46, 7.58, 6.09, 6.50, 6.99, 7.04, 
                     7.21, 7.68, 5.47, 6.35, 6.83, 7.37, 7.10, 6.93, 7.41, 7.90, 
                     9.17, 7.16, 8.72, 7.19, 6.57, 6.00, 8.01, 7.78, 6.36, 7.47, 
                     7.31, 8.51, 8.27, 6.07, 6.13, 8.56, 7.95, 7.16, 8.49, 7.18, 
                     6.90, 7.08, 7.15, 8.30, 7.32, 6.40, 8.03, 6.06, 5.85, 6.95, 
                     6.17, 7.14, 8.00, 7.36, 6.32, 7.11, 6.78, 6.98, 7.47, 6.72, 
                     8.58, 8.19, 8.40, 8.58, 6.23, 7.29, 7.76, 6.98, 8.57
                     ]
    red_numbers = [
                   3.83, 3.61, 3.51, 4.94, 4.17, 3.76, 3.34, 3.7, 4.63, 3.49, 
                   3.87, 3.48, 4.03, 4.24, 2.94, 3.27, 3.15, 4.42, 3.45, 4.01, 
                   5.05, 3.23, 3.48, 4.57, 3.99, 3.84
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
                     [31, 40, 51, 58, 69],
                     [2, 22, 60, 61, 64],
                     [23, 26, 44, 53, 68],
                     [4, 15, 16, 28, 34],
                     [32, 33, 37, 45, 59]
                     ]
    red_numbers = [4, 16, 17, 20, 21]
    return render_template('predictions.html',
                            draw=draw, 
                            white_numbers=white_numbers, 
                            red_numbers=red_numbers
                            )