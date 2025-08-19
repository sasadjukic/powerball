

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
              'all-time': [3015, 3071, 6170],
              'six-months': [195, 195, 400],
              'recent-trends': [63, 61, 130]
            }

    sets = {
            'all-time' : [784, 855, 916, 931, 856, 874, 954, 6170],
            'six-months' : [56, 53, 63, 50, 64, 58, 56, 400],
            'recent-trends' : [22, 17, 15, 19, 20, 15, 22, 130]
    }

    winning_hands = {
                     'singles': [203, 16, 8], 'pairs': [635, 41, 11], 
                     'two_pairs': [233, 13, 4], 'three_of_set': [135, 8, 3], 
                     'full_house': [18, 2, 0], 'poker': [10, 0, 0], 'flush': [0, 0, 0]
                     }
    total_winning_hands = sum(values[0] for values in winning_hands.values())
    total_winning_hands_6 = sum(values[1] for values in winning_hands.values())
    total_winning_hands_recent = sum(values[2] for values in winning_hands.values())

    pair_count = {
                  1: [76, 3, 0], 10: [81, 5, 0], 20: [111, 8, 1], 30: [102, 5, 1], 
                  40: [75, 10, 4], 50: [88, 4, 2], 60: [101, 5, 2]
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
              'all-time': [613, 621, 1234],
              'six-months': [40, 40, 80], 
              'recent-trends': [12, 14, 26]
            }

    sets = {
            'all-time' : [439, 443, 352, 1234],
            'six-months' : [29, 21, 30, 80],
            'recent-trends' : [11, 3, 12, 26]
           }

    return render_template('winning_hands_red.html', 
                           splits=splits,
                           sets=sets
                           )

@powerball.route('/trends', methods=['POST', 'GET'])
def trends():
    white_numbers_6 = [
                       5, 5, 4, 11, 6, 6, 9, 6, 4, 3, 
                       7, 6, 5, 4, 6, 8, 4, 7, 3, 6, 
                       7, 2, 14, 5, 6, 1, 3, 12, 7, 4, 
                       4, 2, 7, 6, 10, 6, 6, 2, 3, 9, 
                       3, 5, 9, 9, 7, 5, 4, 7, 6, 8, 
                       5, 11, 6, 4, 4, 4, 5, 4, 7, 7, 
                       6, 8, 7, 6, 6, 3, 4, 2, 7
                    ]

    white_numbers_trends = [
                        1, 2, 1, 4, 2, 2, 3, 5, 2, 0, 
                        2, 2, 1, 1, 3, 3, 0, 2, 3, 0, 
                        2, 0, 2, 2, 3, 0, 1, 5, 0, 0, 
                        2, 1, 4, 2, 6, 2, 1, 1, 0, 3, 
                        0, 2, 4, 3, 2, 2, 0, 2, 2, 3, 
                        2, 3, 1, 2, 1, 0, 1, 2, 0, 1, 
                        4, 4, 3, 2, 3, 0, 1, 0, 4
                    ]

    red_numbers_6 = [
                     5, 7, 2, 3, 3, 3, 0, 2, 4, 1, 
                     3, 4, 3, 2, 3, 0, 0, 1, 4, 8, 
                     4, 2, 2, 5, 9, 0
                    ]

    red_numbers_trends = [
                          1, 3, 1, 1, 1, 1, 0, 2, 1, 0, 
                          0, 1, 0, 1, 0, 0, 0, 1, 0, 2, 
                          2, 2, 2, 2, 2, 0
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
                     6.99, 7.25, 8.00, 7.58, 6.39, 7.25, 6.85, 6.56, 7.11, 7.11, 
                     7.23, 7.92, 5.10, 6.15, 7.11, 6.91, 7.26, 7.32, 7.02, 7.17, 
                     9.19, 6.14, 8.80, 7.10, 6.80, 6.00, 8.58, 7.68, 6.71, 7.32, 
                     6.76, 8.58, 8.41, 6.16, 6.97, 8.42, 7.75, 6.88, 7.86, 7.16, 
                     6.49, 7.03, 7.30, 7.93, 7.43, 6.34, 7.78, 6.49, 5.67, 7.69, 
                     5.63, 6.89, 7.63, 7.44, 6.77, 7.26, 7.24, 6.50, 7.29, 6.64, 
                     9.11, 8.65, 8.13, 7.82, 6.68, 6.60, 7.15, 7.66, 9.21
                     ]
    red_numbers = [
                   3.84, 3.81, 4.04, 5.04, 4.19, 3.60, 3.23, 3.31, 4.46, 3.59, 
                   3.56, 3.62, 3.44, 4.59, 2.94, 3.16, 3.12, 4.47, 4.04, 3.99, 
                   4.79, 3.42, 3.48, 4.64, 3.94, 3.69
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
                     [7, 17, 34, 55, 63],
                     [25, 50, 59, 62, 66],
                     [5, 18, 38, 39, 51],
                     [11, 19, 35, 43, 68],
                     [3, 6, 13, 48, 52]
                     ]
    red_numbers = [4, 5, 11, 16, 17]
    return render_template('predictions.html',
                            draw=draw, 
                            white_numbers=white_numbers, 
                            red_numbers=red_numbers
                            )