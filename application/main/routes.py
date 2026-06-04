

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
              'all-time': [3317, 3383, 6790],
              'six-months': [190, 204, 400],
              'recent-trends': [52, 76, 130]
            }

    sets = {
            'all-time' : [860, 944, 1007, 1013, 939, 975, 1052, 6790],
            'six-months' : [49, 55, 59, 55, 54, 72, 56, 400],
            'recent-trends' : [12, 15, 14, 24, 24, 19, 22, 130]
    }

    winning_hands = {
                     'singles': [227, 16, 7], 'pairs': [706, 47, 13], 
                     'two_pairs': [251, 11, 4], 'three_of_set': [142, 4, 2], 
                     'full_house': [21, 1, 0], 'poker': [11, 1, 0], 'flush': [0, 0, 0]
                     }
    total_winning_hands = sum(values[0] for values in winning_hands.values())
    total_winning_hands_6 = sum(values[1] for values in winning_hands.values())
    total_winning_hands_recent = sum(values[2] for values in winning_hands.values())

    pair_count = {
                  1: [81, 4, 0], 10: [92, 8, 2], 20: [120, 5, 2], 30: [107, 3, 1], 
                  40: [88, 7, 3], 50: [102, 10, 1], 60: [115, 10, 4]
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
              'all-time': [670, 688, 1358],
              'six-months': [39, 41, 80], 
              'recent-trends': [15, 11, 26]
            }

    sets = {
            'all-time' : [479, 490, 389, 1358],
            'six-months' : [27, 27, 26, 80],
            'recent-trends' : [8, 13, 5, 26]
           }

    return render_template('winning_hands_red.html', 
                           splits=splits,
                           sets=sets
                           )

@powerball.route('/trends', methods=['POST', 'GET'])
def trends():
    white_numbers_6 = [
                       3, 4, 6, 7, 9, 7, 5, 5, 3, 4, 
                       7, 2, 4, 7, 2, 6, 5, 12, 6, 5, 
                       9, 3, 4, 7, 5, 3, 8, 11, 4, 7, 
                       8, 3, 5, 4, 6, 9, 6, 4, 3, 5, 
                       6, 9, 5, 3, 2, 5, 9, 6, 4, 3, 
                       8, 13, 5, 4, 5, 11, 8, 8, 7, 7, 
                       4, 4, 10, 12, 7, 3, 2, 4, 3
                    ]

    white_numbers_trends = [
                        1, 1, 2, 3, 1, 1, 1, 1, 1, 1, 
                        0, 0, 2, 2, 1, 3, 3, 2, 1, 0, 
                        2, 1, 0, 4, 2, 0, 3, 1, 1, 4, 
                        3, 2, 1, 1, 2, 4, 4, 2, 1, 1, 
                        2, 5, 2, 2, 1, 3, 4, 2, 2, 0, 
                        3, 5, 1, 0, 1, 3, 4, 1, 1, 3, 
                        2, 1, 3, 5, 4, 1, 2, 1, 0
                    ]

    red_numbers_6 = [
                     7, 4, 2, 2, 4, 5, 3, 0, 0, 2, 
                     2, 5, 3, 5, 4, 1, 2, 2, 1, 4, 
                     3, 2, 5, 4, 2, 6
                    ]

    red_numbers_trends = [
                          1, 1, 2, 0, 2, 1, 1, 0, 0, 1, 
                          1, 3, 2, 2, 3, 0, 0, 1, 0, 0, 
                          0, 1, 0, 0, 1, 3
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
                     6.82, 7.07, 7.35, 6.76, 6.82, 7.92, 6.93, 6.83, 6.81, 6.84, 
                     7.15, 7.48, 5.16, 6.83, 7.08, 7.33, 6.66, 6.99, 7.52, 7.11, 
                     9.09, 6.45, 8.59, 6.83, 6.35, 6.06, 8.64, 8.67, 6.69, 7.12, 
                     6.98, 8.27, 8.08, 6.17, 6.66, 8.43, 7.63, 6.67, 7.77, 7.69, 
                     6.76, 6.73, 7.12, 7.71, 7.59, 6.11, 8.19, 6.47, 6.35, 6.81, 
                     6.50, 7.59, 7.78, 7.06, 7.09, 7.01, 6.94, 6.42, 8.37, 6.61, 
                     8.75, 7.98, 8.82, 8.75, 6.88, 7.43, 7.02, 6.82, 8.04
                     ]
    red_numbers = [
                   4.57, 3.76, 3.74, 4.74, 4.33, 3.77, 3.25, 3.08, 4.29, 3.88, 
                   3.49, 3.18, 3.46, 4.79, 3.10, 3.09, 3.12, 4.47, 3.35, 4.27, 
                   4.64, 3.31, 3.54, 4.52, 3.93, 4.33
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
                     [14, 16, 33, 61, 65],
                     [34, 41, 45, 48, 69],
                     [3, 25, 29, 44, 52],
                     [7, 21, 25, 53, 69],
                     [1, 28, 38, 64, 67]
                     ]
    red_numbers = [6, 21, 24, 25, 26]
    return render_template('predictions.html',
                            draw=draw, 
                            white_numbers=white_numbers, 
                            red_numbers=red_numbers
                            )