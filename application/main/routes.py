

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
              'all-time': [3108, 3168, 6360],
              'six-months': [198, 194, 400],
              'recent-trends': [62, 68, 130]
            }

    sets = {
            'all-time' : [807, 884, 944, 951, 884, 897, 993, 6360],
            'six-months' : [55, 55, 59, 52, 59, 51, 69, 400],
            'recent-trends' : [18, 19, 17, 13, 19, 16, 28, 130]
    }

    winning_hands = {
                     'singles': [209, 16, 4], 'pairs': [656, 40, 14], 
                     'two_pairs': [239, 14, 4], 'three_of_set': [138, 8, 2], 
                     'full_house': [20, 2, 2], 'poker': [10, 0, 0], 'flush': [0, 0, 0]
                     }
    total_winning_hands = sum(values[0] for values in winning_hands.values())
    total_winning_hands_6 = sum(values[1] for values in winning_hands.values())
    total_winning_hands_recent = sum(values[2] for values in winning_hands.values())

    pair_count = {
                  1: [77, 2, 1], 10: [84, 5, 2], 20: [115, 7, 1], 30: [102, 2, 0], 
                  40: [81, 11, 6], 50: [91, 5, 2], 60: [105, 7, 2]
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
              'all-time': [628, 644, 1272],
              'six-months': [35, 45, 80], 
              'recent-trends': [10, 16, 26]
            }

    sets = {
            'all-time' : [449, 461, 362, 1272],
            'six-months' : [25, 27, 28, 80],
            'recent-trends' : [5, 14, 7, 26]
           }

    return render_template('winning_hands_red.html', 
                           splits=splits,
                           sets=sets
                           )

@powerball.route('/trends', methods=['POST', 'GET'])
def trends():
    white_numbers_6 = [
                       4, 5, 9, 7, 3, 5, 8, 8, 6, 4, 
                       5, 6, 7, 5, 6, 7, 5, 6, 4, 1, 
                       3, 4, 9, 5, 5, 2, 7, 12, 11, 2, 
                       6, 8, 6, 7, 8, 3, 7, 2, 3, 8, 
                       2, 6, 11, 8, 5, 3, 5, 6, 5, 7, 
                       5, 9, 10, 5, 2, 1, 3, 5, 4, 6, 
                       10, 10, 3, 9, 7, 6, 8, 4, 6
                    ]

    white_numbers_trends = [
                        1, 2, 6, 1, 0, 2, 3, 2, 1, 3, 
                        1, 2, 3, 1, 2, 2, 3, 2, 0, 1, 
                        0, 2, 0, 1, 0, 1, 3, 4, 5, 1, 
                        1, 5, 0, 1, 0, 0, 1, 1, 3, 2, 
                        0, 1, 4, 3, 1, 1, 3, 2, 2, 1, 
                        2, 2, 3, 3, 1, 0, 1, 2, 1, 4, 
                        2, 3, 0, 2, 3, 6, 5, 2, 1
                    ]

    red_numbers_6 = [
                     3, 5, 3, 4, 5, 1, 0, 2, 2, 2, 
                     4, 3, 1, 3, 4, 1, 2, 3, 4, 4, 
                     4, 5, 4, 3, 7, 1
                    ]

    red_numbers_trends = [
                          1, 1, 1, 2, 0, 0, 0, 0, 0, 2, 
                          1, 2, 0, 2, 3, 1, 0, 1, 2, 2, 
                          1, 1, 2, 0, 0, 1
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
                     7.29, 7.28, 7.96, 6.84, 6.33, 7.74, 6.43, 6.96, 7.31, 7.02, 
                     7.63, 7.74, 5.26, 6.37, 7.29, 7.52, 7.05, 6.84, 7.26, 7.10, 
                     9.29, 6.68, 8.63, 6.98, 6.22, 5.26, 8.04, 8.39, 7.02, 7.24, 
                     7.12, 8.38, 8.32, 6.36, 6.95, 7.94, 8.01, 6.33, 7.79, 7.11, 
                     6.05, 6.57, 7.86, 8.14, 7.57, 5.86, 8.00, 6.64, 6.20, 7.26, 
                     6.21, 7.32, 7.75, 7.06, 6.93, 6.42, 6.63, 6.41, 7.45, 7.08, 
                     8.93, 8.59, 7.71, 8.25, 6.67, 7.67, 7.69, 7.63, 8.17
                     ]
    red_numbers = [
                   3.88, 3.57, 3.75, 5.05, 4.26, 3.31, 3.35, 3.49, 4.61, 3.54, 
                   3.65, 3.05, 3.38, 4.43, 3.37, 3.36, 3.55, 4.19, 4.08, 4.25, 
                   4.65, 3.23, 3.35, 4.34, 4.53, 3.78
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
                     [8, 15, 44, 48, 61],
                     [6, 21, 28, 29, 33],
                     [12, 25, 36, 54, 69],
                     [5, 60, 62, 67, 68],
                     [3, 18, 23, 31, 40]
                     ]
    red_numbers = [5, 10, 13, 15, 26]
    return render_template('predictions.html',
                            draw=draw, 
                            white_numbers=white_numbers, 
                            red_numbers=red_numbers
                            )