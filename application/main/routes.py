

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
              'all-time': [3488, 3560, 7140],
              'six-months': [193, 204, 400],
              'recent-trends': [70, 59, 130]
            }

    sets = {
            'all-time' : [911, 1001, 1050, 1053, 993, 1038, 1094, 7140],
            'six-months' : [57, 64, 47, 48, 63, 71, 50, 400],
            'recent-trends' : [21, 21, 17, 17, 23, 22, 9, 130]
    }

    winning_hands = {
                     'singles': [235, 11, 0], 'pairs': [740, 40, 11], 
                     'two_pairs': [269, 19, 9], 'three_of_set': [152, 10, 6], 
                     'full_house': [21, 0, 0], 'poker': [11, 0, 0], 'flush': [0, 0, 0]
                     }
    total_winning_hands = sum(values[0] for values in winning_hands.values())
    total_winning_hands_6 = sum(values[1] for values in winning_hands.values())
    total_winning_hands_recent = sum(values[2] for values in winning_hands.values())

    pair_count = {
                  1: [87, 6, 2], 10: [96, 5, 0], 20: [122, 2, 2], 30: [110, 3, 2], 
                  40: [95, 9, 2], 50: [111, 10, 3], 60: [118, 5, 0]
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
              'all-time': [707, 721, 1428],
              'six-months': [42, 38, 80], 
              'recent-trends': [11, 15, 26]
            }

    sets = {
            'all-time' : [506, 515, 407, 1428],
            'six-months' : [27, 33, 20, 80],
            'recent-trends' : [7, 10, 9, 26]
           }

    return render_template('winning_hands_red.html', 
                           splits=splits,
                           sets=sets
                           )

@powerball.route('/trends', methods=['POST', 'GET'])
def trends():
    white_numbers_6 = [
                       3, 7, 9, 10, 7, 5, 3, 7, 6, 5, 
                       3, 4, 8, 10, 6, 10, 8, 5, 5, 3, 
                       8, 3, 4, 4, 5, 6, 3, 4, 7, 6, 
                       5, 6, 3, 5, 3, 5, 6, 7, 2, 6, 
                       6, 8, 2, 11, 6, 4, 4, 9, 7, 10, 
                       5, 3, 6, 6, 9, 7, 9, 8, 8, 5, 
                       6, 2, 3, 8, 8, 5, 5, 4, 4
                    ]

    white_numbers_trends = [
                        2, 3, 2, 5, 2, 1, 2, 2, 2, 0, 
                        2, 1, 4, 2, 3, 2, 2, 3, 2, 0, 
                        4, 1, 3, 2, 1, 2, 0, 1, 3, 2, 
                        1, 3, 2, 3, 1, 2, 2, 1, 0, 1, 
                        3, 5, 0, 4, 3, 1, 1, 2, 3, 3, 
                        4, 1, 1, 2, 3, 3, 3, 1, 1, 1, 
                        1, 0, 0, 2, 1, 1, 0, 2, 1
                    ]

    red_numbers_6 = [
                     2, 4, 6, 3, 3, 1, 3, 1, 4, 4, 
                     2, 4, 5, 6, 3, 1, 3, 3, 2, 5, 
                     2, 2, 5, 1, 4, 1
                    ]

    red_numbers_trends = [
                          1, 0, 0, 1, 1, 0, 2, 0, 2, 1, 
                          1, 0, 2, 2, 1, 0, 1, 0, 2, 3, 
                          2, 0, 2, 1, 1, 0
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
                     6.86, 7.06, 7.69, 6.96, 6.79, 7.43, 6.78, 7.12, 6.55, 6.32, 
                     7.01, 7.15, 5.71, 6.85, 6.95, 7.65, 6.93, 7.72, 7.43, 6.56, 
                     9.04, 6.24, 8.50, 7.27, 6.66, 5.89, 8.74, 8.32, 7.18, 7.39, 
                     7.06, 8.26, 8.43, 6.34, 6.05, 8.19, 7.83, 6.94, 8.24, 7.43, 
                     6.43, 7.90, 6.43, 8.24, 7.44, 5.72, 7.93, 6.56, 5.88, 7.24, 
                     6.14, 7.62, 7.74, 6.86, 7.17, 7.59, 7.12, 7.32, 7.71, 6.81, 
                     8.57, 7.62, 8.41, 8.69, 6.64, 6.75, 6.83, 6.61, 8.51
                ]
    red_numbers = [
                   4.13, 3.94, 3.86, 4.76, 4.09, 3.59, 3.68, 3.20, 4.19, 3.72, 
                   3.36, 2.83, 3.65, 4.72, 3.36, 3.03, 3.35, 4.24, 3.66, 4.59, 
                   4.47, 3.59, 3.66, 4.28, 4.36, 3.69
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
                     [24, 33, 39, 59, 67],
                     [3, 30, 34, 40, 67],
                     [1, 8, 16, 17, 43],
                     [7, 35, 54, 60, 61],
                     [4, 27, 33, 37, 69]
                     ]
    red_numbers = [12, 14, 15, 23, 26]
    return render_template('predictions.html',
                            draw=draw, 
                            white_numbers=white_numbers, 
                            red_numbers=red_numbers
                            )