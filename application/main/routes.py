

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
              'all-time': [3188, 3227, 6500],
              'six-months': [207, 188, 400],
              'recent-trends': [76, 53, 130]
            }

    sets = {
            'all-time' : [827, 904, 970, 972, 894, 926, 1007, 6500],
            'six-months' : [54, 60, 61, 53, 49, 57, 66, 400],
            'recent-trends' : [19, 19, 26, 19, 9, 26, 12, 130]
    }

    winning_hands = {
                     'singles': [216, 16, 6], 'pairs': [674, 46, 17], 
                     'two_pairs': [242, 11, 3], 'three_of_set': [138, 5, 0], 
                     'full_house': [20, 2, 0], 'poker': [10, 0, 0], 'flush': [0, 0, 0]
                     }
    total_winning_hands = sum(values[0] for values in winning_hands.values())
    total_winning_hands_6 = sum(values[1] for values in winning_hands.values())
    total_winning_hands_recent = sum(values[2] for values in winning_hands.values())

    pair_count = {
                  1: [79, 3, 2], 10: [86, 5, 2], 20: [116, 6, 1], 30: [106, 5, 4], 
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
              'all-time': [638, 662, 1300],
              'six-months': [33, 47, 80], 
              'recent-trends': [10, 16, 26]
            }

    sets = {
            'all-time' : [459, 470, 371, 1300],
            'six-months' : [28, 28, 24, 80],
            'recent-trends' : [10, 8, 8, 26]
           }

    return render_template('winning_hands_red.html', 
                           splits=splits,
                           sets=sets
                           )

@powerball.route('/trends', methods=['POST', 'GET'])
def trends():
    white_numbers_6 = [
                       3, 4, 9, 6, 7, 5, 7, 10, 3, 5, 
                       7, 3, 4, 6, 8, 7, 3, 10, 7, 3, 
                       3, 5, 5, 6, 4, 5, 7, 16, 7, 3, 
                       7, 9, 6, 7, 5, 4, 4, 3, 5, 7, 
                       3, 4, 7, 6, 4, 3, 5, 4, 6, 5, 
                       9, 5, 11, 4, 2, 3, 6, 5, 7, 6, 
                       7, 9, 3, 9, 6, 8, 6, 5, 7
                    ]

    white_numbers_trends = [
                        2, 0, 1, 3, 7, 1, 1, 4, 0, 1, 
                        2, 0, 1, 2, 2, 2, 0, 5, 4, 2, 
                        3, 1, 1, 3, 2, 3, 2, 8, 1, 2, 
                        2, 3, 2, 3, 1, 2, 1, 1, 2, 1, 
                        1, 0, 1, 1, 1, 1, 1, 1, 1, 0, 
                        4, 3, 3, 1, 1, 3, 3, 3, 5, 1, 
                        0, 2, 2, 2, 0, 1, 0, 1, 3
                    ]

    red_numbers_6 = [
                     6, 7, 3, 4, 3, 0, 2, 1, 2, 2, 
                     1, 2, 0, 7, 3, 2, 4, 2, 5, 4, 
                     3, 4, 8, 0, 2, 3
                    ]

    red_numbers_trends = [
                          3, 3, 1, 1, 0, 0, 2, 0, 0, 0, 
                          0, 0, 0, 4, 0, 1, 2, 0, 1, 1, 
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
                     6.95, 7.55, 8.22, 7.11, 6.35, 7.86, 6.92, 7.12, 6.59, 6.85, 
                     6.99, 7.58, 5.39, 6.48, 6.86, 7.38, 6.93, 7.43, 7.21, 7.47, 
                     8.57, 6.69, 8.73, 6.68, 6.26, 5.87, 8.42, 8.75, 6.27, 6.92, 
                     6.72, 8.32, 8.58, 6.15, 6.59, 8.15, 8.28, 6.24, 8.30, 8.16, 
                     6.42, 6.48, 7.42, 7.54, 7.07, 6.11, 7.99, 5.97, 5.73, 7.24, 
                     6.34, 7.83, 7.91, 7.11, 6.59, 6.37, 6.93, 6.99, 7.99, 6.91, 
                     8.82, 8.70, 8.09, 8.48, 6.41, 7.52, 7.63, 6.56, 8.96
                     ]
    red_numbers = [
                   4.12, 3.78, 4.07, 4.89, 3.71, 3.55, 3.44, 3.20, 4.30, 3.70, 
                   3.21, 3.24, 3.40, 4.77, 3.36, 3.17, 3.34, 4.51, 4.01, 4.06, 
                   4.70, 3.55, 3.64, 4.25, 4.41, 3.62
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
                     [14, 23, 39, 59, 69],
                     [37, 49, 56, 57, 68],
                     [9, 32, 34, 48, 53],
                     [4, 15, 24, 47, 61],
                     [11, 12, 38, 50, 51]
                     ]
    red_numbers = [2, 11, 13, 15, 22]
    return render_template('predictions.html',
                            draw=draw, 
                            white_numbers=white_numbers, 
                            red_numbers=red_numbers
                            )