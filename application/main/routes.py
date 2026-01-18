

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
              'all-time': [3185, 3225, 6495],
              'six-months': [206, 189, 400],
              'recent-trends': [75, 54, 130]
            }

    sets = {
            'all-time' : [826, 904, 969, 970, 894, 924, 1007, 6495],
            'six-months' : [54, 60, 61, 51, 52, 56, 66, 400],
            'recent-trends' : [18, 20, 25, 18, 10, 26, 13, 130]
    }

    winning_hands = {
                     'singles': [216, 16, 7], 'pairs': [673, 45, 16], 
                     'two_pairs': [242, 11, 3], 'three_of_set': [138, 6, 0], 
                     'full_house': [20, 2, 0], 'poker': [10, 0, 0], 'flush': [0, 0, 0]
                     }
    total_winning_hands = sum(values[0] for values in winning_hands.values())
    total_winning_hands_6 = sum(values[1] for values in winning_hands.values())
    total_winning_hands_recent = sum(values[2] for values in winning_hands.values())

    pair_count = {
                  1: [79, 3, 2], 10: [86, 5, 2], 20: [116, 6, 1], 30: [105, 4, 3], 
                  40: [81, 8, 0], 50: [98, 10, 6], 60: [107, 8, 2]
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
              'all-time': [638, 661, 1299],
              'six-months': [33, 47, 80], 
              'recent-trends': [10, 16, 26]
            }

    sets = {
            'all-time' : [459, 469, 371, 1299],
            'six-months' : [28, 27, 25, 80],
            'recent-trends' : [10, 8, 8, 26]
           }

    return render_template('winning_hands_red.html', 
                           splits=splits,
                           sets=sets
                           )

@powerball.route('/trends', methods=['POST', 'GET'])
def trends():
    white_numbers_6 = [
                       3, 4, 9, 7, 6, 5, 7, 10, 3, 5, 
                       7, 3, 4, 6, 8, 7, 3, 10, 7, 3, 
                       4, 5, 5, 6, 4, 5, 7, 15, 7, 3, 
                       7, 9, 6, 6, 5, 4, 3, 3, 5, 7, 
                       3, 4, 8, 6, 4, 3, 5, 5, 7, 5, 
                       9, 5, 11, 4, 1, 3, 6, 5, 7, 6, 
                       7, 9, 3, 9, 6, 8, 6, 5, 7
                    ]

    white_numbers_trends = [
                        2, 0, 1, 3, 6, 1, 1, 4, 0, 2, 
                        2, 0, 1, 2, 2, 2, 0, 5, 4, 2, 
                        3, 1, 1, 3, 2, 3, 2, 7, 1, 2, 
                        3, 3, 2, 2, 1, 2, 0, 1, 2, 1, 
                        1, 0, 1, 1, 1, 1, 1, 1, 2, 0, 
                        5, 3, 3, 1, 0, 3, 3, 3, 5, 1, 
                        0, 2, 2, 2, 0, 1, 0, 2, 3
                    ]

    red_numbers_6 = [
                     6, 7, 3, 4, 3, 0, 2, 1, 2, 2, 
                     1, 2, 0, 7, 3, 2, 3, 2, 5, 4, 
                     3, 5, 8, 0, 2, 3
                    ]

    red_numbers_trends = [
                          3, 3, 1, 1, 0, 0, 2, 0, 0, 0, 
                          0, 0, 0, 4, 0, 1, 1, 0, 2, 1, 
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
                     7.19, 7.25, 8.23, 6.48, 6.81, 7.84, 6.93, 7.67, 6.43, 6.02, 
                     6.79, 7.70, 5.32, 6.33, 7.05, 7.66, 6.63, 7.47, 7.27, 7.33, 
                     9.22, 6.92, 8.81, 7.09, 6.13, 5.60, 8.47, 8.56, 6.90, 7.14, 
                     7.01, 8.59, 8.28, 5.85, 6.19, 8.37, 7.57, 6.71, 7.87, 7.20, 
                     6.73, 6.26, 7.45, 7.90, 7.67, 6.22, 7.30, 6.76, 5.77, 7.41, 
                     6.13, 7.80, 8.65, 7.36, 6.68, 6.97, 7.26, 6.11, 7.65, 6.23, 
                     8.79, 8.57, 7.76, 8.20, 6.39, 7.87, 7.60, 7.16, 8.47
                     ]
    red_numbers = [
                   4.26, 3.75, 3.82, 4.90, 4.13, 3.28, 3.43, 3.50, 4.22, 3.63, 
                   3.40, 3.11, 3.59, 4.62, 3.09, 2.83, 2.99, 4.38, 3.91, 4.13, 
                   4.67, 3.53, 3.64, 4.44, 4.72, 4.03
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
                     [28, 32, 36, 44, 51],
                     [39, 42, 43, 55, 61],
                     [6, 29, 30, 31, 35],
                     [7, 46, 50, 53, 60],
                     [3, 17, 23, 40, 59]
                     ]
    red_numbers = [3, 8, 9, 18, 24]
    return render_template('predictions.html',
                            draw=draw, 
                            white_numbers=white_numbers, 
                            red_numbers=red_numbers
                            )