

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
              'all-time': [3195, 3234, 6515],
              'six-months': [205, 190, 400],
              'recent-trends': [72, 56, 130]
            }

    sets = {
            'all-time' : [828, 906, 973, 974, 894, 929, 1011, 6515],
            'six-months' : [53, 59, 61, 53, 47, 59, 68, 400],
            'recent-trends' : [17, 18, 26, 18, 9, 27, 15, 130]
    }

    winning_hands = {
                     'singles': [216, 15, 5], 'pairs': [676, 46, 18], 
                     'two_pairs': [243, 12, 3], 'three_of_set': [138, 5, 0], 
                     'full_house': [20, 2, 0], 'poker': [10, 0, 0], 'flush': [0, 0, 0]
                     }
    total_winning_hands = sum(values[0] for values in winning_hands.values())
    total_winning_hands_6 = sum(values[1] for values in winning_hands.values())
    total_winning_hands_recent = sum(values[2] for values in winning_hands.values())

    pair_count = {
                  1: [79, 3, 2], 10: [86, 5, 2], 20: [116, 6, 1], 30: [106, 5, 3], 
                  40: [81, 8, 0], 50: [98, 10, 6], 60: [109, 9, 4]
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
              'all-time': [640, 663, 1303],
              'six-months': [34, 46, 80], 
              'recent-trends': [10, 16, 26]
            }

    sets = {
            'all-time' : [460, 472, 371, 1303],
            'six-months' : [28, 30, 22, 80],
            'recent-trends' : [9, 9, 8, 26]
           }

    return render_template('winning_hands_red.html', 
                           splits=splits,
                           sets=sets
                           )

@powerball.route('/trends', methods=['POST', 'GET'])
def trends():
    white_numbers_6 = [
                       3, 4, 9, 6, 7, 5, 7, 9, 3, 5, 
                       7, 3, 4, 6, 8, 8, 3, 9, 6, 3, 
                       4, 5, 5, 6, 3, 6, 8, 14, 7, 3, 
                       8, 9, 5, 7, 5, 4, 4, 3, 5, 7, 
                       3, 3, 7, 6, 4, 3, 5, 3, 6, 5, 
                       9, 5, 12, 4, 3, 3, 6, 5, 7, 7, 
                       7, 9, 5, 9, 6, 8, 6, 5, 6
                    ]

    white_numbers_trends = [
                        2, 1, 1, 3, 7, 1, 0, 2, 0, 1, 
                        3, 0, 1, 2, 1, 2, 0, 5, 3, 2, 
                        4, 1, 1, 3, 2, 3, 3, 6, 1, 1, 
                        3, 2, 2, 3, 2, 1, 1, 1, 2, 1, 
                        1, 0, 1, 1, 1, 1, 1, 1, 1, 0, 
                        4, 3, 4, 1, 2, 3, 3, 2, 5, 2, 
                        1, 2, 4, 2, 0, 1, 0, 1, 2
                    ]

    red_numbers_6 = [
                     6, 6, 3, 4, 4, 0, 2, 1, 2, 2, 
                     1, 3, 0, 7, 3, 2, 4, 3, 5, 3, 
                     3, 4, 8, 0, 1, 3
                    ]

    red_numbers_trends = [
                          3, 2, 0, 1, 1, 0, 2, 0, 0, 0, 
                          0, 1, 0, 3, 0, 1, 2, 1, 1, 1, 
                          1, 1, 3, 0, 0, 2
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
                     7.01, 7.83, 7.98, 7.14, 6.76, 8.02, 7.29, 7.41, 6.93, 6.51, 
                     7.05, 8.02, 5.63, 6.38, 7.21, 7.29, 6.64, 7.36, 6.83, 7.03, 
                     8.51, 6.31, 8.59, 7.38, 6.18, 5.97, 8.27, 8.85, 6.56, 7.50, 
                     6.63, 8.73, 8.43, 5.72, 6.67, 8.11, 7.90, 6.58, 7.63, 7.33, 
                     6.30, 6.81, 7.02, 7.48, 7.26, 5.60, 7.94, 6.25, 5.95, 6.74, 
                     6.53, 6.81, 8.38, 7.12, 6.72, 6.62, 7.16, 6.51, 8.28, 6.76, 
                     9.32, 7.89, 7.93, 8.95, 6.52, 7.89, 7.74, 6.69, 8.66
                     ]
    red_numbers = [
                   3.55, 4.04, 4.01, 4.97, 4.38, 3.40, 3.12, 3.60, 4.30, 3.62, 
                   3.63, 3.36, 3.71, 4.74, 3.15, 2.82, 3.50, 4.96, 3.55, 4.11, 
                   4.70, 3.28, 3.49, 4.18, 3.93, 3.90
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
                     [5, 26, 57, 58, 62],
                     [1, 2, 17, 22, 53],
                     [25, 30, 51, 60, 61],
                     [19, 38, 44, 64, 65],
                     [4, 18, 23, 24, 59]
                     ]
    red_numbers = [5, 9, 13, 19, 25]
    return render_template('predictions.html',
                            draw=draw, 
                            white_numbers=white_numbers, 
                            red_numbers=red_numbers
                            )