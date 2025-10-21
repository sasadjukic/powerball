

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
              'all-time': [3087, 3134, 6305],
              'six-months': [203, 188, 400],
              'recent-trends': [71, 59, 130]
            }

    sets = {
            'all-time' : [798, 879, 938, 946, 874, 889, 981, 6305],
            'six-months' : [53, 60, 59, 54, 59, 49, 66, 400],
            'recent-trends' : [14, 24, 22, 14, 18, 14, 24, 130]
    }

    winning_hands = {
                     'singles': [206, 13, 3], 'pairs': [649, 40, 14], 
                     'two_pairs': [239, 15, 6], 'three_of_set': [137, 9, 1], 
                     'full_house': [20, 3, 2], 'poker': [10, 0, 0], 'flush': [0, 0, 0]
                     }
    total_winning_hands = sum(values[0] for values in winning_hands.values())
    total_winning_hands_6 = sum(values[1] for values in winning_hands.values())
    total_winning_hands_recent = sum(values[2] for values in winning_hands.values())

    pair_count = {
                  1: [76, 1, 0], 10: [84, 6, 3], 20: [115, 9, 4], 30: [102, 3, 0], 
                  40: [78, 10, 3], 50: [90, 5, 2], 60: [103, 5, 2]
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
              'all-time': [625, 636, 1261],
              'six-months': [36, 44, 80], 
              'recent-trends': [11, 15, 26]
            }

    sets = {
            'all-time' : [448, 457, 356, 1261],
            'six-months' : [27, 25, 28, 80],
            'recent-trends' : [8, 14, 4, 26]
           }

    return render_template('winning_hands_red.html', 
                           splits=splits,
                           sets=sets
                           )

@powerball.route('/trends', methods=['POST', 'GET'])
def trends():
    white_numbers_6 = [
                       6, 4, 8, 7, 4, 3, 8, 8, 5, 5, 
                       5, 5, 7, 7, 9, 9, 3, 6, 4, 2, 
                       4, 3, 10, 4, 6, 2, 7, 12, 9, 3, 
                       6, 7, 7, 8, 9, 3, 7, 2, 2, 9, 
                       3, 7, 8, 7, 7, 4, 4, 6, 4, 7, 
                       5, 8, 8, 4, 2, 2, 3, 4, 6, 5, 
                       9, 8, 5, 9, 6, 6, 7, 3, 8
                    ]

    white_numbers_trends = [
                        1, 1, 6, 0, 0, 0, 2, 3, 1, 3, 
                        3, 1, 3, 3, 3, 4, 1, 2, 1, 1, 
                        0, 3, 2, 1, 1, 1, 4, 5, 4, 1, 
                        1, 5, 1, 3, 0, 0, 2, 1, 0, 2, 
                        2, 3, 0, 2, 2, 1, 3, 1, 2, 2, 
                        1, 1, 5, 2, 1, 0, 0, 1, 1, 1, 
                        4, 2, 0, 5, 1, 4, 4, 1, 2
                    ]

    red_numbers_6 = [
                     3, 6, 3, 4, 5, 1, 0, 2, 3, 2, 
                     3, 2, 2, 3, 3, 1, 2, 2, 5, 5, 
                     4, 4, 2, 5, 8, 0
                    ]

    red_numbers_trends = [
                          1, 1, 1, 2, 2, 0, 0, 0, 1, 2, 
                          0, 1, 0, 2, 2, 1, 2, 1, 3, 1, 
                          0, 2, 0, 0, 1, 0
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
                     7.37, 7.32, 7.17, 6.63, 6.11, 7.41, 7.04, 6.84, 6.72, 6.55, 
                     7.24, 8.06, 5.62, 6.55, 7.18, 7.59, 7.74, 7.06, 7.09, 7.58, 
                     8.62, 7.33, 8.74, 6.94, 6.33, 5.84, 8.63, 8.14, 7.08, 7.25, 
                     7.24, 8.56, 8.27, 6.15, 6.63, 9.09, 7.72, 6.64, 7.52, 7.27, 
                     6.74, 6.87, 6.71, 7.59, 7.33, 6.07, 7.70, 5.43, 5.65, 7.17, 
                     6.38, 7.65, 8.19, 7.32, 6.29, 7.20, 6.77, 6.35, 8.05, 6.67, 
                     9.04, 8.15, 8.12, 8.87, 6.19, 7.30, 7.51, 7.37, 8.46
                     ]
    red_numbers = [
                   3.83, 3.95, 3.56, 5.14, 4.32, 3.44, 3.22, 3.32, 4.41, 3.41, 
                   3.57, 3.36, 3.75, 4.82, 3.11, 3.16, 2.96, 4.69, 3.93, 4.39, 
                   4.67, 3.28, 3.37, 4.30, 4.10, 3.94
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
                     [17, 19, 29, 43, 52],
                     [10, 11, 26, 55, 61],
                     [5, 32, 62, 65, 67],
                     [24, 35, 45, 50, 51],
                     [1, 31, 39, 56, 58]
                     ]
    red_numbers = [7, 12, 15, 20, 26]
    return render_template('predictions.html',
                            draw=draw, 
                            white_numbers=white_numbers, 
                            red_numbers=red_numbers
                            )