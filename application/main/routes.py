

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
              'all-time': [3104, 3162, 6350],
              'six-months': [199, 193, 400],
              'recent-trends': [62, 68, 130]
            }

    sets = {
            'all-time' : [805, 883, 943, 950, 882, 895, 992, 6350],
            'six-months' : [54, 56, 60, 52, 60, 49, 69, 400],
            'recent-trends' : [16, 20, 17, 14, 20, 16, 27, 130]
    }

    winning_hands = {
                     'singles': [208, 15, 3], 'pairs': [655, 40, 14], 
                     'two_pairs': [239, 15, 5], 'three_of_set': [138, 8, 2], 
                     'full_house': [20, 2, 2], 'poker': [10, 0, 0], 'flush': [0, 0, 0]
                     }
    total_winning_hands = sum(values[0] for values in winning_hands.values())
    total_winning_hands_6 = sum(values[1] for values in winning_hands.values())
    total_winning_hands_recent = sum(values[2] for values in winning_hands.values())

    pair_count = {
                  1: [76, 1, 0], 10: [84, 5, 2], 20: [115, 8, 1], 30: [102, 2, 0], 
                  40: [81, 11, 6], 50: [91, 5, 3], 60: [105, 7, 2]
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
              'all-time': [628, 642, 1270],
              'six-months': [36, 44, 80], 
              'recent-trends': [11, 15, 26]
            }

    sets = {
            'all-time' : [449, 461, 360, 1270],
            'six-months' : [25, 28, 27, 80],
            'recent-trends' : [6, 15, 5, 26]
           }

    return render_template('winning_hands_red.html', 
                           splits=splits,
                           sets=sets
                           )

@powerball.route('/trends', methods=['POST', 'GET'])
def trends():
    white_numbers_6 = [
                       4, 5, 9, 7, 4, 4, 7, 8, 6, 4, 
                       5, 5, 7, 5, 7, 8, 5, 6, 4, 2, 
                       3, 4, 9, 5, 5, 2, 7, 13, 10, 2, 
                       6, 8, 6, 7, 8, 3, 7, 2, 3, 8, 
                       3, 7, 10, 8, 5, 3, 4, 7, 5, 7, 
                       4, 9, 9, 5, 2, 1, 3, 5, 4, 7, 
                       10, 10, 3, 9, 6, 6, 8, 4, 6
                    ]

    white_numbers_trends = [
                        1, 2, 6, 1, 0, 1, 2, 2, 1, 3, 
                        1, 1, 3, 2, 3, 2, 3, 2, 0, 1, 
                        0, 2, 0, 1, 0, 1, 3, 5, 4, 1, 
                        1, 6, 0, 1, 0, 0, 2, 1, 2, 2, 
                        0, 3, 3, 3, 1, 1, 2, 2, 3, 2, 
                        1, 2, 3, 3, 1, 0, 1, 2, 1, 4, 
                        2, 3, 0, 2, 2, 6, 5, 2, 1
                    ]

    red_numbers_6 = [
                     3, 5, 3, 4, 5, 1, 0, 2, 2, 2, 
                     4, 3, 2, 3, 4, 1, 2, 3, 4, 4, 
                     4, 5, 3, 3, 7, 1
                    ]

    red_numbers_trends = [
                          2, 1, 1, 2, 0, 0, 0, 0, 0, 2, 
                          1, 2, 0, 2, 3, 1, 0, 1, 3, 2, 
                          0, 1, 1, 0, 0, 1
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
                     6.67, 7.72, 7.90, 6.61, 6.05, 7.11, 6.49, 7.06, 7.22, 6.96, 
                     6.98, 7.66, 5.00, 6.51, 7.11, 7.47, 7.18, 7.22, 7.12, 7.10, 
                     9.28, 6.75, 8.82, 6.61, 6.56, 5.89, 8.35, 7.89, 6.31, 6.47, 
                     6.86, 8.17, 8.92, 6.44, 6.33, 7.93, 7.84, 6.59, 7.65, 7.92, 
                     6.65, 6.82, 7.15, 8.01, 7.69, 5.88, 7.74, 6.43, 6.00, 6.98, 
                     6.39, 7.52, 8.20, 7.28, 6.59, 6.74, 7.19, 6.79, 7.81, 6.82, 
                     8.58, 8.05, 8.31, 8.76, 6.47, 7.74, 7.95, 7.82, 8.92
                     ]
    red_numbers = [
                   4.08, 3.78, 3.7, 5.32, 4.39, 3.62, 2.95, 3.22, 4.45, 3.55, 
                   3.68, 3.29, 3.82, 4.1, 3.23, 2.68, 3.44, 4.42, 3.67, 4.27, 
                   4.70, 3.35, 3.37, 4.68, 4.60, 3.64
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
                     [1, 10, 15, 33, 48],
                     [17, 25, 31, 53, 60],
                     [32, 42, 61, 64, 69],
                     [28, 37, 44, 55, 67],
                     [11, 14, 26, 50, 52]
                     ]
    red_numbers = [1, 7, 12, 20, 21]
    return render_template('predictions.html',
                            draw=draw, 
                            white_numbers=white_numbers, 
                            red_numbers=red_numbers
                            )