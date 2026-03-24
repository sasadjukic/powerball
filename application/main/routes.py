

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
              'all-time': [3253, 3294, 6635],
              'six-months': [205, 191, 400],
              'recent-trends': [62, 65, 130]
            }

    sets = {
            'all-time' : [843, 924, 992, 988, 911, 951, 1026, 6635],
            'six-months' : [53, 59, 65, 49, 46, 68, 60, 400],
            'recent-trends' : [16, 19, 20, 16, 17, 23, 19, 130]
    }

    winning_hands = {
                     'singles': [219, 14, 3], 'pairs': [689, 46, 15], 
                     'two_pairs': [247, 12, 4], 'three_of_set': [140, 4, 2], 
                     'full_house': [21, 3, 1], 'poker': [11, 1, 1], 'flush': [0, 0, 0]
                     }
    total_winning_hands = sum(values[0] for values in winning_hands.values())
    total_winning_hands_6 = sum(values[1] for values in winning_hands.values())
    total_winning_hands_recent = sum(values[2] for values in winning_hands.values())

    pair_count = {
                  1: [80, 4, 1], 10: [89, 7, 3], 20: [118, 4, 2], 30: [106, 4, 0], 
                  40: [84, 9, 3], 50: [100, 10, 2], 60: [111, 8, 4]
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
              'all-time': [654, 673, 1327],
              'six-months': [36, 44, 80], 
              'recent-trends': [15, 11, 26]
            }

    sets = {
            'all-time' : [470, 477, 380, 1327],
            'six-months' : [26, 30, 24, 80],
            'recent-trends' : [11, 6, 9, 26]
           }

    return render_template('winning_hands_red.html', 
                           splits=splits,
                           sets=sets
                           )

@powerball.route('/trends', methods=['POST', 'GET'])
def trends():
    white_numbers_6 = [
                       3, 5, 9, 4, 8, 7, 6, 8, 3, 6, 
                       5, 4, 4, 6, 4, 6, 5, 12, 7, 6, 
                       6, 5, 4, 4, 3, 5, 8, 16, 8, 5, 
                       6, 8, 5, 4, 4, 6, 3, 3, 5, 6, 
                       2, 4, 6, 4, 2, 3, 8, 6, 5, 4, 
                       9, 9, 7, 6, 4, 7, 5, 10, 7, 8, 
                       3, 5, 7, 7, 5, 9, 5, 6, 5
                    ]

    white_numbers_trends = [
                        0, 3, 2, 0, 1, 4, 2, 2, 2, 1, 
                        1, 2, 0, 3, 0, 2, 2, 5, 3, 3, 
                        3, 2, 3, 0, 1, 0, 2, 4, 2, 3, 
                        2, 0, 2, 0, 3, 4, 1, 1, 0, 3, 
                        1, 3, 1, 0, 0, 1, 4, 3, 1, 3, 
                        2, 4, 0, 3, 1, 4, 0, 5, 1, 3, 
                        1, 1, 5, 3, 2, 1, 0, 2, 1
                    ]

    red_numbers_6 = [
                     7, 5, 2, 4, 2, 4, 2, 0, 0, 3, 
                     2, 4, 1, 6, 4, 2, 2, 2, 4, 4, 
                     4, 2, 8, 3, 0, 3
                    ]

    red_numbers_trends = [
                          3, 1, 0, 1, 2, 4, 0, 0, 0, 1, 
                          1, 1, 1, 0, 1, 0, 0, 1, 0, 2, 
                          2, 0, 2, 3, 0, 0
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
                     6.94, 7.20, 7.61, 6.81, 6.56, 7.46, 6.74, 7.14, 6.79, 6.28, 
                     7.10, 7.89, 5.17, 6.48, 7.02, 7.39, 6.94, 7.22, 7.45, 7.15, 
                     8.81, 6.49, 8.82, 7.11, 6.13, 5.65, 8.53, 8.88, 6.42, 7.18, 
                     7.53, 8.01, 8.39, 6.20, 6.82, 8.44, 7.66, 6.66, 8.27, 7.51, 
                     6.17, 6.83, 7.08, 7.41, 7.44, 6.40, 7.98, 6.40, 6.06, 6.75, 
                     6.32, 8.20, 8.13, 7.11, 6.68, 6.77, 7.01, 6.69, 7.69, 7.41, 
                     9.07, 7.63, 8.45, 8.55, 6.44, 7.26, 7.51, 7.16, 8.55
                     ]
    red_numbers = [
                   4.04, 3.65, 3.58, 4.92, 4.44, 3.65, 3.63, 3.22, 4.14, 3.35, 
                   3.56, 3.24, 3.62, 4.61, 3.25, 2.94, 3.05, 4.32, 4.01, 4.01, 
                   4.81, 3.64, 3.70, 4.66, 4.46, 3.50
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
                     [10, 34, 40, 41, 55],
                     [4, 12, 27, 48, 50],
                     [3, 46, 49, 60, 69],
                     [23, 30, 31, 52, 66],
                     [24, 29, 37, 39, 51]
                     ]
    red_numbers = [1, 4, 9, 15, 25]
    return render_template('predictions.html',
                            draw=draw, 
                            white_numbers=white_numbers, 
                            red_numbers=red_numbers
                            )