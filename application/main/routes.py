

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
              'all-time': [2979, 3036, 6095],
              'six-months': [196, 197, 400],
              'recent-trends': [65, 61, 130]
            }

    sets = {
            'all-time' : [772, 844, 908, 919, 842, 869, 941, 6095],
            'six-months' : [55, 53, 62, 52, 62, 63, 53, 400],
            'recent-trends' : [19, 14, 21, 20, 17, 22, 17, 130]
    }

    winning_hands = {
                     'singles': [200, 15, 7], 'pairs': [628, 40, 11], 
                     'two_pairs': [231, 16, 6], 'three_of_set': [132, 7, 2], 
                     'full_house': [18, 2, 0], 'poker': [10, 0, 0], 'flush': [0, 0, 0]
                     }
    total_winning_hands = sum(values[0] for values in winning_hands.values())
    total_winning_hands_6 = sum(values[1] for values in winning_hands.values())
    total_winning_hands_recent = sum(values[2] for values in winning_hands.values())

    pair_count = {
                  1: [76, 4, 1], 10: [81, 8, 2], 20: [110, 8, 1], 30: [101, 4, 1], 
                  40: [73, 8, 3], 50: [88, 4, 2], 60: [99, 4, 1]
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
              'all-time': [605, 614, 1219],
              'six-months': [40, 40, 80], 
              'recent-trends': [11, 15, 26]
            }

    sets = {
            'all-time' : [431, 442, 346, 1219],
            'six-months' : [29, 25, 26, 80],
            'recent-trends' : [6, 8, 12, 26]
           }

    return render_template('winning_hands_red.html', 
                           splits=splits,
                           sets=sets
                           )

@powerball.route('/trends', methods=['POST', 'GET'])
def trends():
    white_numbers_6 = [
                       5, 6, 5, 9, 7, 7, 7, 6, 3, 3, 
                       5, 8, 5, 4, 5, 9, 6, 6, 2, 6, 
                       7, 2, 14, 4, 5, 1, 4, 10, 9, 5, 
                       4, 6, 6, 5, 7, 5, 8, 2, 4, 8, 
                       4, 4, 7, 9, 7, 4, 7, 5, 7, 7, 
                       4, 12, 8, 6, 5, 4, 5, 5, 7, 8, 
                       5, 8, 6, 5, 5, 5, 3, 2, 6
                    ]

    white_numbers_trends = [
                        3, 1, 1, 2, 3, 1, 3, 2, 3, 0, 
                        0, 3, 4, 1, 0, 2, 2, 1, 1, 0, 
                        2, 0, 5, 1, 3, 0, 2, 4, 4, 1, 
                        2, 2, 3, 3, 4, 1, 4, 0, 0, 2, 
                        0, 2, 4, 3, 2, 1, 1, 2, 0, 3, 
                        1, 7, 1, 2, 1, 1, 1, 3, 2, 1, 
                        3, 3, 2, 2, 1, 0, 2, 1, 2
                    ]

    red_numbers_6 = [
                     4, 4, 2, 3, 4, 4, 1, 2, 5, 1, 
                     3, 4, 3, 3, 3, 0, 1, 3, 4, 8, 
                     3, 1, 1, 5, 8, 0
                    ]

    red_numbers_trends = [
                          0, 1, 1, 0, 2, 1, 0, 1, 0, 0, 
                          3, 1, 1, 0, 1, 0, 0, 1, 1, 1, 
                          2, 1, 0, 3, 5, 0
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
                     7.23, 7.05, 7.02, 7.14, 6.85, 7.66, 6.96, 6.01, 6.52, 6.65, 
                     6.92, 7.65, 5.24, 6.66, 6.33, 7.85, 7.11, 6.52, 7.28, 7.66, 
                     9.17, 6.72, 9.72, 7.08, 6.81, 5.76, 8.25, 8.19, 6.43, 7.41, 
                     6.85, 8.14, 8.84, 6.03, 6.66, 8.31, 7.93, 7.28, 7.98, 7.34, 
                     6.51, 6.74, 7.26, 7.81, 7.77, 5.87, 7.74, 6.54, 5.96, 7.17, 
                     6.09, 7.54, 8.16, 7.24, 6.29, 6.84, 6.74, 6.76, 8.19, 6.23, 
                     9.16, 8.36, 8.51, 8.03, 6.13, 7.16, 7.92, 7.36, 8.71
                     ]
    red_numbers = [
                   4.07, 3.30, 4.07, 4.70, 4.10, 4.13, 3.24, 3.29, 3.99, 3.41, 
                   3.69, 3.41, 3.79, 4.58, 3.10, 2.89, 3.38, 4.44, 3.79, 4.19, 
                   4.46, 3.58, 3.17, 5.20, 4.21, 3.82
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
                     [20, 23, 33, 55, 69],
                     [3, 8, 30, 31, 46],
                     [5, 14, 29, 37, 44],
                     [2, 22, 36, 42, 68],
                     [10, 29, 61, 65, 66]
                     ]
    red_numbers = [1, 5, 7, 17, 21]
    return render_template('predictions.html',
                            draw=draw, 
                            white_numbers=white_numbers, 
                            red_numbers=red_numbers
                            )