

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
              'all-time': [3069, 3122, 6275],
              'six-months': [199, 192, 400],
              'recent-trends': [65, 65, 130]
            }

    sets = {
            'all-time' : [796, 870, 934, 942, 870, 886, 977, 6275],
            'six-months' : [54, 52, 63, 53, 62, 50, 66, 400],
            'recent-trends' : [15, 19, 21, 12, 20, 13, 30, 130]
    }

    winning_hands = {
                     'singles': [205, 15, 3], 'pairs': [646, 39, 13], 
                     'two_pairs': [239, 15, 7], 'three_of_set': [137, 9, 3], 
                     'full_house': [18, 2, 0], 'poker': [10, 0, 0], 'flush': [0, 0, 0]
                     }
    total_winning_hands = sum(values[0] for values in winning_hands.values())
    total_winning_hands_6 = sum(values[1] for values in winning_hands.values())
    total_winning_hands_recent = sum(values[2] for values in winning_hands.values())

    pair_count = {
                  1: [76, 1, 0], 10: [82, 4, 1], 20: [115, 10, 5], 30: [102, 3, 0], 
                  40: [77, 10, 3], 50: [90, 5, 2], 60: [103, 5, 2]
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
              'all-time': [622, 633, 1255],
              'six-months': [37, 43, 80], 
              'recent-trends': [12, 14, 26]
            }

    sets = {
            'all-time' : [448, 451, 356, 1255],
            'six-months' : [30, 22, 28, 80],
            'recent-trends' : [12, 9, 5, 26]
           }

    return render_template('winning_hands_red.html', 
                           splits=splits,
                           sets=sets
                           )

@powerball.route('/trends', methods=['POST', 'GET'])
def trends():
    white_numbers_6 = [
                       6, 4, 8, 9, 4, 3, 8, 7, 5, 3, 
                       4, 5, 4, 6, 9, 9, 3, 5, 4, 4, 
                       4, 4, 12, 5, 6, 2, 5, 11, 10, 5, 
                       6, 5, 7, 7, 9, 3, 8, 1, 2, 8, 
                       3, 8, 9, 7, 8, 5, 3, 6, 5, 7, 
                       5, 8, 9, 3, 3, 2, 3, 3, 7, 5, 
                       9, 10, 5, 8, 6, 6, 7, 3, 7
                    ]

    white_numbers_trends = [
                        1, 1, 5, 1, 0, 1, 3, 2, 1, 1, 
                        3, 1, 0, 3, 4, 4, 1, 1, 1, 0, 
                        0, 3, 4, 2, 1, 1, 2, 4, 4, 1, 
                        2, 3, 2, 2, 0, 0, 2, 0, 0, 4, 
                        2, 3, 0, 2, 2, 2, 2, 0, 3, 3, 
                        1, 0, 5, 1, 1, 0, 0, 0, 2, 2, 
                        5, 4, 1, 5, 3, 3, 3, 2, 2
                    ]

    red_numbers_6 = [
                     4, 7, 3, 5, 5, 1, 0, 2, 3, 1, 
                     3, 1, 2, 2, 2, 1, 2, 2, 6, 5, 
                     4, 4, 2, 5, 8, 0
                    ]

    red_numbers_trends = [
                          2, 2, 1, 3, 3, 0, 0, 0, 1, 0, 
                          0, 0, 0, 2, 1, 1, 2, 1, 2, 1, 
                          0, 2, 1, 0, 1, 0
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
                     7.29, 7.43, 7.76, 6.69, 6.11, 7.39, 7.18, 6.81, 6.69, 6.55, 
                     7.31, 7.72, 4.71, 6.31, 6.82, 7.38, 7.49, 6.32, 7.79, 7.78, 
                     8.91, 6.91, 9.23, 7.19, 6.18, 5.44, 8.03, 8.20, 6.79, 6.96, 
                     7.19, 8.53, 8.42, 6.38, 6.46, 8.27, 7.57, 6.30, 7.56, 7.84, 
                     6.75, 6.80, 7.29, 7.89, 7.85, 5.92, 7.86, 6.78, 5.95, 7.80, 
                     6.21, 6.97, 8.01, 7.09, 6.56, 7.13, 6.70, 6.75, 7.74, 6.51, 
                     9.38, 8.67, 8.20, 8.21, 6.31, 7.45, 7.29, 7.19, 8.85
                     ]
    red_numbers = [
                   3.87, 3.61, 3.90, 4.86, 4.25, 3.42, 3.37, 3.75, 4.14, 3.49, 
                   3.47, 3.16, 4.10, 4.76, 3.14, 2.98, 3.42, 4.68, 3.79, 4.12, 
                   4.53, 3.04, 3.24, 4.90, 4.30, 3.71
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
                     [5, 8, 13, 41, 44],
                     [25, 42, 43, 47, 54],
                     [24, 45, 53, 59, 63],
                     [3, 18, 20, 40, 67],
                     [9, 19, 35, 36, 38]
                     ]
    red_numbers = [5, 7, 22, 24, 26]
    return render_template('predictions.html',
                            draw=draw, 
                            white_numbers=white_numbers, 
                            red_numbers=red_numbers
                            )