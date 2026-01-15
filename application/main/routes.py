

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
              'all-time': [3182, 3223, 6490],
              'six-months': [205, 190, 400],
              'recent-trends': [74, 55, 130]
            }

    sets = {
            'all-time' : [824, 904, 968, 970, 893, 924, 1007, 6490],
            'six-months' : [53, 61, 60, 51, 53, 55, 67, 400],
            'recent-trends' : [17, 20, 24, 19, 9, 27, 14, 130]
    }

    winning_hands = {
                     'singles': [216, 16, 7], 'pairs': [672, 45, 16], 
                     'two_pairs': [242, 11, 3], 'three_of_set': [138, 6, 0], 
                     'full_house': [20, 2, 0], 'poker': [10, 0, 0], 'flush': [0, 0, 0]
                     }
    total_winning_hands = sum(values[0] for values in winning_hands.values())
    total_winning_hands_6 = sum(values[1] for values in winning_hands.values())
    total_winning_hands_recent = sum(values[2] for values in winning_hands.values())

    pair_count = {
                  1: [78, 2, 1], 10: [86, 5, 2], 20: [116, 6, 1], 30: [105, 4, 3], 
                  40: [81, 9, 0], 50: [98, 10, 7], 60: [107, 8, 2]
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
              'all-time': [638, 660, 1298],
              'six-months': [33, 47, 80], 
              'recent-trends': [10, 16, 26]
            }

    sets = {
            'all-time' : [459, 468, 371, 1298],
            'six-months' : [28, 26, 26, 80],
            'recent-trends' : [10, 7, 9, 26]
           }

    return render_template('winning_hands_red.html', 
                           splits=splits,
                           sets=sets
                           )

@powerball.route('/trends', methods=['POST', 'GET'])
def trends():
    white_numbers_6 = [
                       3, 4, 9, 7, 5, 5, 7, 10, 3, 5, 
                       7, 4, 4, 6, 8, 7, 3, 10, 7, 3, 
                       4, 5, 5, 6, 4, 5, 6, 15, 7, 3,
                       7, 9, 6, 6, 5, 4, 3, 3, 5, 7, 
                       3, 4, 8, 6, 5, 4, 5, 5, 6, 5, 
                       9, 5, 11, 4, 1, 3, 5, 5, 7, 6, 
                       7, 9, 4, 9, 6, 8, 6, 5, 7
                    ]

    white_numbers_trends = [
                        2, 0, 1, 3, 5, 1, 2, 3, 0, 2, 
                        2, 0, 1, 2, 2, 2, 0, 5, 4, 2, 
                        3, 1, 1, 3, 2, 3, 1, 7, 1, 2, 
                        3, 3, 3, 2, 1, 2, 0, 1, 2, 1, 
                        1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 
                        5, 3, 3, 1, 0, 3, 3, 3, 5, 1, 
                        0, 2, 2, 2, 0, 2, 0, 2, 3
                    ]

    red_numbers_6 = [
                     6, 7, 3, 4, 3, 0, 2, 1, 2, 2, 
                     1, 2, 0, 6, 3, 2, 3, 2, 5, 4, 
                     3, 5, 8, 1, 2, 3
                    ]

    red_numbers_trends = [
                          3, 3, 1, 1, 0, 0, 2, 0, 0, 0, 
                          0, 0, 0, 3, 0, 1, 1, 0, 2, 1, 
                          1, 1, 4, 0, 0, 2
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
                     7.76, 7.09, 8.16, 6.95, 6.65, 7.34, 6.88, 6.83, 6.33, 6.85, 
                     7.59, 7.59, 5.34, 6.42, 7.47, 7.36, 7.05, 7.61, 7.14, 7.38, 
                     8.93, 7.06, 8.78, 7.56, 6.03, 5.45, 8.07, 8.68, 6.66, 6.96, 
                     7.19, 8.89, 8.26, 6.32, 6.75, 8.16, 7.95, 6.55, 8.15, 7.53, 
                     6.42, 6.65, 7.61, 7.76, 7.37, 5.66, 8.12, 6.27, 5.48, 6.99, 
                     6.97, 6.98, 8.04, 7.01, 6.76, 6.67, 6.64, 6.48, 7.45, 6.52, 
                     8.36, 8.57, 7.65, 8.22, 6.32, 7.75, 7.57, 7.45, 8.54
                     ]
    red_numbers = [
                   4.03, 3.65, 3.64, 4.98, 4.12, 3.92, 3.36, 3.49, 4.21, 3.38, 
                   3.46, 3.35, 3.76, 4.77, 2.85, 3.05, 3.16, 4.13, 4.11, 4.21, 
                   4.33, 3.51, 4.02, 4.48, 4.31, 3.72
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
                     [3, 9, 10, 17, 62],
                     [19, 25, 33, 55, 61],
                     [12, 18, 39, 46, 68],
                     [5, 23, 29, 52, 60],
                     [4, 15, 16, 57, 67]
                     ]
    red_numbers = [11, 16, 17, 18, 24]
    return render_template('predictions.html',
                            draw=draw, 
                            white_numbers=white_numbers, 
                            red_numbers=red_numbers
                            )